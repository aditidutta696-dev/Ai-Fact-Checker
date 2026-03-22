import json
import os
from difflib import SequenceMatcher

FACTS_FILE = "facts.json"

# 🔹 Load facts from file
def load_facts():
    if not os.path.exists(FACTS_FILE):
        return []

    with open(FACTS_FILE, "r", encoding="utf-8") as f:
        print("✅ FACTS LOADED:", len(FACTS))
        return json.load(f)


# 🔹 Normalize text
def normalize(text):
    return text.lower().replace(".", "").strip()


# 🔹 Retrieve relevant facts



# Load facts once
with open("facts.json", "r") as f:
    FACTS = json.load(f)

print("✅ FACTS LOADED:", len(FACTS))


def retrieve(query: str, top_k=5):

    query_words = set(query.lower().split())

    results = []

    for fact in FACTS_FILE:
        fact_words = set(fact.lower().split())

        # 🔹 SIMPLE WORD OVERLAP SIMILARITY
        common = query_words.intersection(fact_words)

        if len(query_words) > 0:
            score = len(common) / len(query_words)
        else:
            score = 0

        # 🔹 FILTER (IMPORTANT)
        if score > 0.2:
            results.append((fact, score))

    # 🔹 SORT BEST MATCHES
    results.sort(key=lambda x: x[1], reverse=True)

    print("📦 Retrieved:", results[:top_k])

    return results[:top_k]
# 🔹 Add new fact
def add_fact(fact: str):
    facts = load_facts()
    facts.append(fact)

    with open(FACTS_FILE, "w", encoding="utf-8") as f:
        json.dump(facts, f, indent=4)


# 🔹 Save fact (same as add)
def save_fact_to_file(fact: str):
    add_fact(fact)