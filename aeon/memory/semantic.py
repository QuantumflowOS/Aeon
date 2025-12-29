import math

class SemanticMemory:
    """
    Lightweight vector store (FAISS can replace this drop-in).
    """

    def __init__(self):
        self.items = []  # (text, vector)

    def _embed(self, text: str):
        # deterministic toy embedding (replace with OpenAI/FAISS later)
        return [len(text), sum(ord(c) for c in text) % 1000]

    def add(self, text: str):
        self.items.append((text, self._embed(text)))

    def similarity(self, a, b):
        return 1 / (1 + math.dist(a, b))

    def query(self, text, k=3):
        qv = self._embed(text)
        scored = [
            (self.similarity(qv, v), t)
            for t, v in self.items
        ]
        return sorted(scored, reverse=True)[:k]
