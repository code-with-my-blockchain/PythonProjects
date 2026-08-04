import json
import time
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from app.core.config import settings
from app.services.faiss_service import faiss_service
from app.models.conversation import Conversation, Message
from app.models.user import User


SYSTEM_PROMPT = """You are a helpful Enterprise AI Knowledge Assistant. 
You answer questions based ONLY on the provided context from the organization's documents.

Rules:
1. Use only the information given in the context.
2. If the answer is not in the context, say "I could not find relevant information in the knowledge base."
3. Be concise, accurate and professional.
4. When possible, mention the source document name.
5. Do not make up information.
6. Support follow-up questions using conversation history.
"""


class RAGService:

    def __init__(self):
        self.llm = ChatGroq(
            model=settings.GROQ_MODEL,
            api_key=settings.GROQ_API_KEY,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
        )

    def retrieve(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        top_k = top_k or settings.TOP_K
        results = faiss_service.search(query, top_k=top_k)
        return results

    def build_context(self, retrieved: List[Dict[str, Any]]) -> str:
        if not retrieved:
            return "No relevant documents found."

        context_parts = []
        for i, item in enumerate(retrieved, 1):
            source = f"[Source {i}: {item.get('document_title', 'Unknown')} | File: {item.get('filename', '')}]"
            context_parts.append(f"{source}\n{item.get('text', '')}")
        
        return "\n\n---\n\n".join(context_parts)

    def build_messages(
        self,
        question: str,
        context: str,
        history: List[Message] = None
    ) -> List:
        messages = [SystemMessage(content=SYSTEM_PROMPT)]

        if history:
            for msg in history[-6:]:
                if msg.role == "user":
                    messages.append(HumanMessage(content=msg.content))
                elif msg.role == "assistant":
                    messages.append(AIMessage(content=msg.content))

        user_content = f"""Context from knowledge base:

{context}

---

User Question: {question}

Answer based on the context above:"""

        messages.append(HumanMessage(content=user_content))
        return messages

    def generate_answer(
        self,
        question: str,
        top_k: int = None,
        history: List[Message] = None
    ) -> Tuple[str, List[Dict[str, Any]], int]:
        start = time.time()

        retrieved = self.retrieve(question, top_k=top_k)
        context = self.build_context(retrieved)
        messages = self.build_messages(question, context, history)

        response = self.llm.invoke(messages)
        answer = response.content if hasattr(response, "content") else str(response)

        elapsed_ms = int((time.time() - start) * 1000)
        return answer, retrieved, elapsed_ms

    def chat(
        self,
        db: Session,
        user: User,
        question: str,
        conversation_id: Optional[int] = None,
        top_k: Optional[int] = None,
    ) -> Dict[str, Any]:
        if conversation_id:
            conversation = db.query(Conversation).filter(
                Conversation.id == conversation_id,
                Conversation.user_id == user.id
            ).first()
            if not conversation:
                raise ValueError("Conversation not found")
        else:
            title = question[:80] + ("..." if len(question) > 80 else "")
            conversation = Conversation(title=title, user_id=user.id)
            db.add(conversation)
            db.commit()
            db.refresh(conversation)

        history = db.query(Message).filter(
            Message.conversation_id == conversation.id
        ).order_by(Message.created_at.asc()).all()

        answer, sources, response_time_ms = self.generate_answer(
            question=question,
            top_k=top_k,
            history=history
        )

        user_msg = Message(
            conversation_id=conversation.id,
            role="user",
            content=question
        )
        db.add(user_msg)

        sources_data = [
            {
                "document_id": s.get("document_id"),
                "document_title": s.get("document_title"),
                "filename": s.get("filename"),
                "chunk_index": s.get("chunk_index"),
                "text": s.get("text", "")[:500],
                "score": s.get("score", 0)
            }
            for s in sources
        ]

        assistant_msg = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=answer,
            sources=json.dumps(sources_data, ensure_ascii=False),
            response_time_ms=response_time_ms
        )
        db.add(assistant_msg)
        db.commit()
        db.refresh(assistant_msg)

        return {
            "answer": answer,
            "sources": sources_data,
            "conversation_id": conversation.id,
            "message_id": assistant_msg.id,
            "response_time_ms": response_time_ms
        }


rag_service = RAGService()
