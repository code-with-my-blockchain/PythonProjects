from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an AI assistant.

Answer ONLY from the provided context.

If the answer is not available in the context, simply reply:

I don't know.
"""
        ),
        (
            "human",
            """
Question:

{question}

Context:

{context}
"""
        )
    ]
)