import numpy as np


def average_embeddings(embeddings):
    if not embeddings:
        return None
    stacked = np.stack(embeddings, axis=0)
    avg = np.mean(stacked, axis=0)
    norm = np.linalg.norm(avg)
    if norm > 0:
        avg = avg / norm
    return avg


def embedding_to_bytes(embedding):
    if embedding is None:
        raise ValueError("embedding is None")
    arr = np.asarray(embedding)
    if arr.size == 0:
        raise ValueError("embedding is empty")
    return arr.astype(np.float32).tobytes()


def bytes_to_embedding(data, dim=512):
    arr = np.frombuffer(data, dtype=np.float32)
    return arr


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    if a is None or b is None:
        return 0.0
    a = np.asarray(a, dtype=np.float32)
    b = np.asarray(b, dtype=np.float32)
    if a.size == 0 or b.size == 0:
        return 0.0
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))
