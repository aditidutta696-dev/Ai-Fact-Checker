import numpy as np

class VectorStore:
    def __init__(self):
        self.vectors = []
        self.texts = []

    def add(self, text, vector):
        self.texts.append(text)
        self.vectors.append(vector)

    def search(self, query_vector, top_k=3):
        sims = []

        for vec in self.vectors:
            sim = np.dot(query_vector, vec) / (
                np.linalg.norm(query_vector) * np.linalg.norm(vec)
            )
            sims.append(sim)

        top_indices = np.argsort(sims)[-top_k:][::-1]

        return [(self.texts[i], float(sims[i])) for i in top_indices]