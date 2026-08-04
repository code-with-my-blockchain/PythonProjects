import os
import pickle
from typing import List, Dict, Optional, Any
from pathlib import Path

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from app.core.config import settings


class FAISSService:
    def __init__(self):
        self.index_path = Path(settings.FAISS_INDEX_PATH)
        self.index_path.mkdir(parents=True, exist_ok=True)
        
        self.index_file = self.index_path / "index.faiss"
        self.metadata_file = self.index_path / "metadata.pkl"
        
       
        print(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
        self.embeddings = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.dimension = self.embeddings.get_sentence_embedding_dimension()
        
        self.index: Optional[faiss.Index] = None
        self.metadata: List[Dict[str, Any]] = []
        
        self._load_index()

    def _load_index(self):
        """Load existing FAISS index and metadata if available"""
        if self.index_file.exists() and self.metadata_file.exists():
            try:
                self.index = faiss.read_index(str(self.index_file))
                with open(self.metadata_file, "rb") as f:
                    self.metadata = pickle.load(f)
                print(f" FAISS index loaded: {self.index.ntotal} vectors")
            except Exception as e:
                print(f" Failed to load index: {e}. Creating new index.")
                self._create_new_index()
        else:
            self._create_new_index()

    def _create_new_index(self):
        """Create a new empty FAISS index"""
        self.index = faiss.IndexFlatIP(self.dimension)
        self.metadata = []
        print(" New FAISS index created")

    def _get_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings and normalize for cosine similarity"""
        vectors = self.embeddings.encode(texts, show_progress_bar=False)
        vectors = np.array(vectors, dtype=np.float32)
        faiss.normalize_L2(vectors)
        return vectors

    def add_documents(
        self,
        chunks: List[str],
        document_id: int,
        document_title: str,
        filename: str,
        metadata_list: Optional[List[Dict]] = None
    ) -> int:
        """Add document chunks to FAISS index."""
        if not chunks:
            return 0

        vectors = self._get_embeddings(chunks)

        if self.index.ntotal == 0 and vectors.shape[1] != self.dimension:
            self.dimension = vectors.shape[1]
            self.index = faiss.IndexFlatIP(self.dimension)

        self.index.add(vectors)

        for i, chunk in enumerate(chunks):
            meta = {
                "document_id": document_id,
                "document_title": document_title,
                "filename": filename,
                "chunk_index": i,
                "text": chunk,
            }
            if metadata_list and i < len(metadata_list):
                meta.update(metadata_list[i])
            self.metadata.append(meta)

        self._save_index()
        return len(chunks)

    def search(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        """Search for similar chunks"""
        top_k = top_k or settings.TOP_K
        
        if self.index is None or self.index.ntotal == 0:
            return []

        query_vector = self._get_embeddings([query])
        
        scores, indices = self.index.search(query_vector, min(top_k, self.index.ntotal))
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(self.metadata):
                continue
            result = self.metadata[idx].copy()
            result["score"] = float(score)
            results.append(result)
        
        return results

    def delete_document(self, document_id: int) -> int:
        """Delete all chunks of a document (rebuilds index)."""
        if not self.metadata:
            return 0

        new_metadata = [m for m in self.metadata if m.get("document_id") != document_id]
        removed_count = len(self.metadata) - len(new_metadata)

        if removed_count == 0:
            return 0

        if not new_metadata:
            self._create_new_index()
            self._save_index()
            return removed_count

        texts = [m["text"] for m in new_metadata]
        vectors = self._get_embeddings(texts)
        
        self.dimension = vectors.shape[1]
        self.index = faiss.IndexFlatIP(self.dimension)
        self.index.add(vectors)
        self.metadata = new_metadata
        
        self._save_index()
        return removed_count

    def _save_index(self):
        """Save index and metadata to disk"""
        faiss.write_index(self.index, str(self.index_file))
        with open(self.metadata_file, "wb") as f:
            pickle.dump(self.metadata, f)

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_vectors": self.index.ntotal if self.index else 0,
            "total_documents": len(set(m["document_id"] for m in self.metadata)),
            "dimension": self.dimension,
            "index_path": str(self.index_path)
        }


faiss_service = FAISSService()
