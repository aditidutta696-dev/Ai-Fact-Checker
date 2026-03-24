#pipeline_manager.py
from api.retrieval.retriever import retrieve
from api.verification.optimization.fluff_flutter import remove_fluff

from reasoning_layer.freshness_guard import check_freshness
from reasoning_layer.conflict_resolver import resolve_conflicts
from reasoning_layer.fact_ranker import rank_facts
from reasoning_layer.decision_engine import make_decision

from performance_layer.cache_manager import get, set


def run_pipeline(query: str):

    try:
        # 🔹 Cache
        cached = get(query)
        if cached:
            return cached

        # 🔹 Step 1: Clean query
        cleaned_query = remove_fluff(query)

        # 🔹 Step 2: Retrieve facts
        raw_results = retrieve(cleaned_query)
        raw_results = raw_results[:3]
        print("\n Retrieved result :",raw_results)

        if not raw_results:
            return {
                "overall_verdict": "UNVERIFIED",
                "confidence": 0,
                "details": []
            }

        # 🔹 Step 3: Convert format
        facts = []
        for i, (text, similarity) in enumerate(raw_results):
            facts.append({
                "id": i,
                "text": text,
                "similarity": similarity,
                "credibility": 0.7,
                "timestamp": "2024-01-01"
            })

        # 🔹 Step 4: Full reasoning pipeline
        facts = [check_freshness(f) for f in facts]
        facts = resolve_conflicts(facts)
        facts = rank_facts(facts)

        # 🔹 Step 5: Decision
        decision = make_decision(facts)

        # ✅ Fallback if decision fails
        if not decision:
            scores = []
            for f in facts:
                sim = f.get("similarity", 0)
                cred = f.get("credibility", 0.5)
                scores.append(sim * cred)

            avg_score = sum(scores) / len(scores) if scores else 0

            if avg_score > 0.75:
                verdict = "SUPPORTED"
            elif avg_score > 0.5:
                verdict = "PARTIALLY_SUPPORTED"
            elif avg_score > 0.3:
                verdict = "UNCERTAIN"
            else:
                verdict = "REFUTED"

            result = {
                "overall_verdict": verdict,
                "confidence": round(avg_score, 2),
                "details": facts
            }

            set(query, result)
            return result
        

        result = {
            "overall_verdict": decision.get("verdict", "UNVERIFIED"),
            "confidence": decision.get("confidence", 0),
            "details": facts
        }

        set(query, result)
        return result

    except Exception as e:
        print("❌ Pipeline Error:", str(e))

        return {
            "overall_verdict": "ERROR",
            "confidence": 0,
            "details": []
        }