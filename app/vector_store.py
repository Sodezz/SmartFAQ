import os
import json
from typing import List, Dict, Any

import numpy as np

try:
    from fastembed import TextEmbedding
except Exception as e:
    TextEmbedding = None  # type: ignore


class SimpleVectorStore:
    def __init__(self, index_dir: str) -> None:
        self.index_dir = index_dir
        os.makedirs(self.index_dir, exist_ok=True)

        self.embeddings_path = os.path.join(self.index_dir, "embeddings.npy")
        self.metadata_path = os.path.join(self.index_dir, "metadata.jsonl")
        # fastembed valid defaults: "BAAI/bge-small-en-v1.5" or multilingual "BAAI/bge-m3"
        self.model_name = os.environ.get("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")

        self._embedding_model = None
        self._embeddings: np.ndarray | None = None
        self._metadatas: List[Dict[str, Any]] = []
        self._texts: List[str] = []

    def _ensure_model(self) -> None:
        if self._embedding_model is None:
            if TextEmbedding is None:
                raise RuntimeError("fastembed is not installed or failed to import")
            self._embedding_model = TextEmbedding(model_name=self.model_name)

    def load(self) -> None:
        if os.path.exists(self.embeddings_path) and os.path.exists(self.metadata_path):
            self._embeddings = np.load(self.embeddings_path)
            self._metadatas = []
            self._texts = []
            with open(self.metadata_path, "r", encoding="utf-8") as f:
                for line in f:
                    obj = json.loads(line)
                    self._metadatas.append(obj["metadata"])  # type: ignore
                    self._texts.append(obj["text"])  # type: ignore
        else:
            self._embeddings = None
            self._metadatas = []
            self._texts = []

    def save(self) -> None:
        if self._embeddings is None:
            return
        np.save(self.embeddings_path, self._embeddings)
        with open(self.metadata_path, "w", encoding="utf-8") as f:
            for text, meta in zip(self._texts, self._metadatas):
                f.write(json.dumps({"text": text, "metadata": meta}, ensure_ascii=False) + "\n")

    def size(self) -> int:
        return 0 if self._embeddings is None else int(self._embeddings.shape[0])

    def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]]) -> None:
        assert len(texts) == len(metadatas)
        if not texts:
            return
        self._ensure_model()

        # Compute embeddings (L2-normalized for cosine similarity via dot product)
        embeddings_iter = self._embedding_model.embed(texts)  # type: ignore
        new_emb_list = [np.array(vec, dtype=np.float32) for vec in embeddings_iter]
        new_emb = np.vstack(new_emb_list)
        norms = np.linalg.norm(new_emb, axis=1, keepdims=True) + 1e-10
        new_emb = new_emb / norms

        if self._embeddings is None:
            self._embeddings = new_emb
            self._metadatas = list(metadatas)
            self._texts = list(texts)
        else:
            self._embeddings = np.vstack([self._embeddings, new_emb])
            self._metadatas.extend(metadatas)
            self._texts.extend(texts)

    def query(self, question: str, top_k: int = 5) -> List[Dict[str, Any]]:
        if self._embeddings is None or self._embeddings.shape[0] == 0:
            return []
        self._ensure_model()

        q_vec_iter = self._embedding_model.embed([question])  # type: ignore
        q_vec = np.array(list(q_vec_iter)[0], dtype=np.float32)
        q_vec = q_vec / (np.linalg.norm(q_vec) + 1e-10)

        # Cosine similarity via dot product since all vectors are normalized
        scores = np.dot(self._embeddings, q_vec)
        top_k = max(1, min(int(top_k), self._embeddings.shape[0]))
        idx = np.argpartition(-scores, top_k - 1)[:top_k]
        # Sort selected indices by score desc
        idx = idx[np.argsort(-scores[idx])]

        results: List[Dict[str, Any]] = []
        for i in idx:
            results.append({
                "score": float(scores[i]),
                "text": self._texts[int(i)],
                "metadata": self._metadatas[int(i)],
            })
        return results

    def reset(self) -> None:
        self._embeddings = None
        self._metadatas = []
        self._texts = []
        # Remove files
        for path in [self.embeddings_path, self.metadata_path]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    pass