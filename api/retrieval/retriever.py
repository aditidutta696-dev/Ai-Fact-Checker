import os
import json
from api.retrieval.vector_store import VectorStore
from api.retrieval.embedder import get_embedding

# 🔹 Initialize vector store
store = VectorStore()

# 🔹 Correct path to facts.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FACT_PATH = os.path.join(BASE_DIR, "../data/facts.json")


# 🔹 Load facts into vector store (ONLY ONCE)
def load_facts():
    try:
        with open(FACT_PATH, "r") as f:
            facts = json.load(f)

        for fact in facts:
            vector = get_embedding(fact)
            store.add(fact, vector)

        print("✅ Facts loaded successfully:", len(facts))

    except Exception as e:
        print("❌ Error loading facts:", e)


# 🔹 Call load once
load_facts()


# 🔹 Retrieve similar facts
def retrieve(query: str, top_k=3):
    try:
        query_vector = get_embedding(query)

        results = store.search(query_vector, top_k=top_k)

        # 🔥 DEBUG PRINT (VERY IMPORTANT)
        print("\n🔍 QUERY:", query)
        print("🔍 RETRIEVED:", results)

        return results

    except Exception as e:
        print("❌ Retrieval error:", e)
        return []


# 🔹 Add fact dynamically
def add_fact(fact: str):
    vector = get_embedding(fact)
    store.add(fact, vector)


# 🔹 Save to file
def save_fact_to_file(fact: str):
    try:
        with open(FACT_PATH, "r") as f:
            data = json.load(f)

        data.append(fact)

        with open(FACT_PATH, "w") as f:
            json.dump(data, f, indent=4)

    except Exception as e:
        print("❌ Save error:", e)