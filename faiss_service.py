import os
import pickle
from typing import List, Dict, Any, Optional
import numpy as np

try:
    import faiss
    from sentence_transformers import SentenceTransformer
except ImportError:
    faiss = None
    SentenceTransformer = None


class FAISSService:
    def __init__(self, index_path: str = "faiss_index.pkl", embedding_model: str = "all-MiniLM-L6-v2"):
        self.index_path = index_path
        self.embedding_model_name = embedding_model
        self.model = None
        self.index = None
        self.documents = []  

        self._initialize_model()
        self.load_index()

    def _initialize_model(self):
        if SentenceTransformer is not None:
            try:
                self.model = SentenceTransformer(self.embedding_model_name)
            except Exception as e:
                print(f"Warning: Could not load SentenceTransformer: {e}")

    def add_texts(self, texts: List[str], metadatas: Optional[List[Dict[str, Any]]] = None) -> bool:
        """Add text chunks and metadata to FAISS index."""
        if not texts:
            return False

        if self.model is None:
            print("Warning: SentenceTransformer model is not initialized.")
            return False

        
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        dimension = embeddings.shape[1]

        
        if self.index is None and faiss is not None:
            self.index = faiss.IndexFlatL2(dimension)

        if self.index is not None:
            self.index.add(np.array(embeddings).astype("float32"))

        
        if metadatas is None:
            metadatas = [{} for _ in texts]

        for text, meta in zip(texts, metadatas):
            self.documents.append({"content": text, "metadata": meta})

        self.save_index()
        return True

    def save_index(self):
        """Save FAISS index and documents metadata to disk."""
        try:
            with open(self.index_path, "wb") as f:
                pickle.dump({"index": self.index, "documents": self.documents}, f)
        except Exception as e:
            print(f"Error saving FAISS index: {e}")

    def load_index(self):
        """Load FAISS index from disk if available."""
        if os.path.exists(self.index_path):
            try:
                with open(self.index_path, "rb") as f:
                    data = pickle.load(f)
                    self.index = data.get("index")
                    self.documents = data.get("documents", [])
            except Exception as e:
                print(f"Error loading FAISS index: {e}")



faiss_service = FAISSService()
