# aeon/core/advanced_memory.py
"""
Advanced memory system with FAISS for efficient similarity search
and persistent storage capabilities.
"""

import numpy as np
import pickle
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    logging.warning("FAISS not available. Install with: pip install faiss-cpu")

from sentence_transformers import SentenceTransformer


class AdvancedSemanticMemory:
    """
    Enhanced semantic memory with FAISS indexing and persistence.
    """
    
    def __init__(self, model_name="all-MiniLM-L6-v2", dimension=384, use_faiss=True):
        self.model = SentenceTransformer(model_name)
        self.dimension = dimension
        self.use_faiss = use_faiss and FAISS_AVAILABLE
        
        # Storage
        self.memories = []  # List of {"text": str, "metadata": dict, "timestamp": str}
        self.vectors = []   # List of embeddings
        
        # FAISS index
        if self.use_faiss:
            self.index = faiss.IndexFlatL2(dimension)
            logging.info("FAISS index initialized")
        else:
            self.index = None
            logging.info("Using fallback memory (no FAISS)")
    
    def store(self, text: str, metadata: Optional[Dict] = None):
        """Store a memory with its embedding."""
        # Generate embedding
        vector = self.model.encode(text)
        
        # Store memory
        memory = {
            "text": text,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow().isoformat()
        }
        self.memories.append(memory)
        self.vectors.append(vector)
        
        # Add to FAISS index
        if self.use_faiss:
            self.index.add(np.array([vector], dtype=np.float32))
        
        logging.debug(f"Stored memory: {text[:50]}...")
        return len(self.memories) - 1
    
    def query(self, text: str, top_k: int = 5, threshold: float = None) -> List[Dict]:
        """
        Query memories by similarity.
        Returns top_k most similar memories with scores.
        """
        if not self.memories:
            return []
        
        # Generate query embedding
        query_vector = self.model.encode(text)
        
        if self.use_faiss:
            # FAISS search
            distances, indices = self.index.search(
                np.array([query_vector], dtype=np.float32), 
                min(top_k, len(self.memories))
            )
            
            results = []
            for dist, idx in zip(distances[0], indices[0]):
                if idx < len(self.memories):
                    similarity = 1 / (1 + dist)  # Convert distance to similarity
                    if threshold is None or similarity >= threshold:
                        results.append({
                            **self.memories[idx],
                            "similarity": float(similarity),
                            "index": int(idx)
                        })
        else:
            # Fallback: numpy cosine similarity
            similarities = []
            for i, vec in enumerate(self.vectors):
                sim = np.dot(query_vector, vec) / (
                    np.linalg.norm(query_vector) * np.linalg.norm(vec)
                )
                similarities.append((sim, i))
            
            similarities.sort(reverse=True)
            results = []
            for sim, idx in similarities[:top_k]:
                if threshold is None or sim >= threshold:
                    results.append({
                        **self.memories[idx],
                        "similarity": float(sim),
                        "index": idx
                    })
        
        return results
    
    def get_recent(self, n: int = 10) -> List[Dict]:
        """Get n most recent memories."""
        return self.memories[-n:]
    
    def get_by_metadata(self, key: str, value: Any) -> List[Dict]:
        """Filter memories by metadata."""
        return [
            m for m in self.memories 
            if m["metadata"].get(key) == value
        ]
    
    def save(self, filepath: str):
        """Save memory to disk."""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "memories": self.memories,
            "vectors": [v.tolist() for v in self.vectors],
            "dimension": self.dimension
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        
        logging.info(f"Memory saved to {filepath}")
    
    def load(self, filepath: str):
        """Load memory from disk."""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        self.memories = data["memories"]
        self.vectors = [np.array(v) for v in data["vectors"]]
        self.dimension = data["dimension"]
        
        # Rebuild FAISS index
        if self.use_faiss and self.vectors:
            self.index = faiss.IndexFlatL2(self.dimension)
            vectors_array = np.array(self.vectors, dtype=np.float32)
            self.index.add(vectors_array)
        
        logging.info(f"Memory loaded from {filepath} ({len(self.memories)} items)")
    
    def clear(self):
        """Clear all memories."""
        self.memories = []
        self.vectors = []
        if self.use_faiss:
            self.index = faiss.IndexFlatL2(self.dimension)
        logging.info("Memory cleared")
    
    def __len__(self):
        return len(self.memories)
    
    def __repr__(self):
        return f"AdvancedSemanticMemory({len(self.memories)} memories, FAISS={self.use_faiss})"


class MemoryConsolidation:
    """
    Consolidates and organizes memories over time.
    Implements forgetting curves and importance weighting.
    """
    
    def __init__(self, memory: AdvancedSemanticMemory):
        self.memory = memory
        self.access_counts = {}  # Track how often memories are accessed
        self.importance_scores = {}  # Manual importance ratings
    
    def access(self, memory_index: int):
        """Record memory access."""
        self.access_counts[memory_index] = self.access_counts.get(memory_index, 0) + 1
    
    def set_importance(self, memory_index: int, score: float):
        """Set importance score (0-1)."""
        self.importance_scores[memory_index] = max(0.0, min(1.0, score))
    
    def get_importance(self, memory_index: int) -> float:
        """Calculate composite importance score."""
        base_importance = self.importance_scores.get(memory_index, 0.5)
        access_bonus = min(0.3, self.access_counts.get(memory_index, 0) * 0.05)
        return base_importance + access_bonus
    
    def consolidate(self, threshold: float = 0.3):
        """
        Remove low-importance memories that haven't been accessed recently.
        Returns number of memories removed.
        """
        indices_to_keep = []
        
        for i in range(len(self.memory)):
            importance = self.get_importance(i)
            if importance >= threshold:
                indices_to_keep.append(i)
        
        # Rebuild memory with only important items
        new_memories = [self.memory.memories[i] for i in indices_to_keep]
        new_vectors = [self.memory.vectors[i] for i in indices_to_keep]
        
        removed_count = len(self.memory) - len(new_memories)
        
        self.memory.memories = new_memories
        self.memory.vectors = new_vectors
        
        # Rebuild FAISS index
        if self.memory.use_faiss and new_vectors:
            self.memory.index = faiss.IndexFlatL2(self.memory.dimension)
            vectors_array = np.array(new_vectors, dtype=np.float32)
            self.memory.index.add(vectors_array)
        
        logging.info(f"Consolidated memory: removed {removed_count} low-importance items")
        return removed_count
    
    def get_statistics(self) -> Dict:
        """Get memory statistics."""
        if not self.memory.memories:
            return {"total": 0}
        
        importances = [self.get_importance(i) for i in range(len(self.memory))]
        
        return {
            "total": len(self.memory),
            "avg_importance": np.mean(importances),
            "max_importance": np.max(importances),
            "min_importance": np.min(importances),
            "total_accesses": sum(self.access_counts.values())
        }
