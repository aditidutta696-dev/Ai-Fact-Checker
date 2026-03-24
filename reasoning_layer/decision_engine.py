from shared.config.settings import DECISION_THRESHOLD_HIGH, DECISION_THRESHOLD_LOW

def make_decision(facts):
    if not facts:
        return {"verdict": "UNVERIFIED", "confidence": 0}

    top_facts = facts[:3]
    scores = [f["score"] for f in top_facts]

    avg_score = sum(scores) / len(scores)

    # 🔥 NEW: detect contradiction pattern
    if avg_score < 0.3:
        verdict = "REFUTED"
    elif avg_score < 0.5:
        verdict = "UNCERTAIN"
    elif avg_score < 0.7:
        verdict = "PARTIALLY_SUPPORTED"
    else:
        verdict = "SUPPORTED"

    return {
        "verdict": verdict,
        "confidence": round(avg_score, 2),
        "fact_id": top_facts[0]["id"]
    }