🧠 FactCheck AI System

A modular AI-powered fact-checking system that analyzes user queries, retrieves relevant facts, detects contradictions, and produces a final verdict such as SUPPORTED, REFUTED, PARTIALLY_SUPPORTED, or UNCERTAIN.

---

🚀 Project Overview

This project is designed to simulate a real-world fact verification pipeline using:

- Semantic search (embeddings)
- Vector similarity
- Rule-based contradiction detection
- Multi-step reasoning pipeline
- FastAPI interface

---

🧩 System Architecture

User Query
   ↓
Preprocessing (ScaleDown API / Cleaning)
   ↓
Claim Splitting
   ↓
Retriever (Vector Search)
   ↓
Reasoning Layer
   ↓
Decision Engine
   ↓
Final Verdict

---

📁 Project Structure

project/
│
├── api/
│   ├── main.py                # FastAPI entry point
│   ├── test/
│   │   └── pipeline_helper.py
│   ├── retrieval/
│   │   ├── retriever.py
│   │   ├── embedder.py
│   │   ├── vector_store.py
│   │   └── facts.json
│
├── orchestrator/
│   └── pipeline_manager.py
│
├── reasoning_layer/
│   ├── freshness_guard.py
│   ├── conflict_resolver.py
│   ├── fact_ranker.py
│   └── decision_engine.py
│
├── performance_layer/
│   └── cache_manager.py

---

⚙️ Core Components

🔹 1. FastAPI Server ("main.py")

- Accepts user queries via "/check"
- Cleans query using ScaleDown API
- Sends processed query to pipeline

---

🔹 2. Pipeline Manager ("pipeline_manager.py")

Handles the full reasoning pipeline:

run_pipeline(query)

Steps:

1. Cache check
2. Query cleaning
3. Fact retrieval
4. Fact formatting
5. Reasoning layer processing
6. Decision making

---

🔹 3. Pipeline Helper ("pipeline_helper.py")

Main interface for:

- Splitting queries into claims
- Evaluating each claim
- Combining results

Key Functions:

- "split_into_claims()"
- "evaluate_claim()"
- "detect_contradictions()"
- "process_claim()"

---

🔹 4. Retriever System

📌 "retriever.py"

- Loads facts from "facts.json"
- Converts facts into embeddings
- Performs similarity search

---

📌 "embedder.py"

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    return model.encode(text)

---

📌 "vector_store.py"

- Stores embeddings
- Computes cosine similarity

sim = dot(a, b) / (||a|| * ||b||)

---

🧠 Logic Design

✅ Fact Matching

- Uses semantic similarity
- Top-K results selected

---

⚠️ Contradiction Detection

Checks:

- Negation mismatch ("not", "no", "does not")
- Word mismatch

---

🔥 Negation Handling (Key Feature)

Fixes errors like:

Claim| Fact| Result
"Water does not boil"| "Water boils"| REFUTED

---

📊 Confidence Scoring

final_conf = base_conf - penalty

---

🏁 Verdict Logic

if final_conf > 0.7:
    SUPPORTED
elif > 0.5:
    PARTIALLY_SUPPORTED
elif > 0.3:
    UNCERTAIN
else:
    REFUTED

---

📦 Dataset ("facts.json")

Stores known facts:

{
  "facts": [
    "The Earth revolves around the Sun.",
    "Water boils at 100 degrees Celsius.",
    "India won the 2011 Cricket World Cup.",
    "Climate change is influenced by human activities."
  ]
}

---

🧪 Example Usage

Input:

The Earth revolves around the Sun and the Sun revolves around the Earth.

Output:

{
  "overall_verdict": "PARTIALLY_SUPPORTED",
  "details": [
    {"claim": "...", "verdict": "SUPPORTED"},
    {"claim": "...", "verdict": "REFUTED"}
  ]
}

---

▶️ How to Run

1. Install dependencies

pip install fastapi uvicorn sentence-transformers numpy

---

2. Run server

uvicorn api.main:app --reload

---

3. Test API

POST request to:

http://127.0.0.1:8000/check

Body:

{
  "query": "The Earth revolves around the Sun"
}

---

💡 Features

✔ Multi-claim analysis
✔ Semantic fact retrieval
✔ Negation-aware reasoning
✔ Modular pipeline design
✔ FastAPI integration
✔ Cache optimization

---

⚠️ Limitations

- Rule-based contradiction detection (not fully semantic)
- Depends on quality of "facts.json"
- Embedding similarity may confuse opposite meanings without negation handling

---

🚀 Future Improvements

- Advanced NLP contradiction detection
- Larger knowledge base
- Real-time web fact retrieval
- Explainable AI outputs
- Confidence calibration

---

👩‍💻 Author Notes

This project demonstrates:

- AI pipeline design
- Information retrieval
- Reasoning systems
- Backend API development

---

🎯 Conclusion

This system is a mini fact-checking engine combining:

- Retrieval
- Reasoning
- Decision making

It is ideal for:

- Academic projects
- AI demos
- Learning NLP pipelines

---

⭐ Final Status

✅ Working
✅ Stable
✅ Demo-ready
✅ Extensible

---

End of README
