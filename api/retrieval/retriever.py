import json
from .embedder import get_embedding
from .vector_store import VectorStore

store = VectorStore()

# Load initial facts (optional)
def load_facts():
    try:
        with open("data/facts.json") as f:
            facts = json.load(f)

        for fact in facts:
            add_fact(fact)

    except FileNotFoundError:
        pass


def add_fact(fact: str):
    emb = get_embedding(fact)
    store.add(fact, emb)


def retrieve(query: str):
    q_emb = get_embedding(query)
    return store.search(q_emb)