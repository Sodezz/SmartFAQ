import numpy
from sentence_transformers import SentenceTransformer



model = SentenceTransformer('all-MiniLM-L6-v2')

def vectorized_document(text: str) -> str:
    vector = model.encode(text)
    return ','.join(map(str, vector))

def cosine_similarity(vec1: str, vec2: str) -> float:
    vec1 = numpy.array([float(x) for x in vec1.split(',')])
    vec2 = numpy.array([float(x) for x in vec2.split(',')])
    return numpy.dot(vec1, vec2) / (numpy.linalg.norm(vec1) * numpy.linalg.norm(vec2))