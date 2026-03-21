from shared.config.settings import DECISION_THRESHOLD_HIGH, DECISION_THRESHOLD_LOW

def make_decision(facts):
    if not facts:
        return {"verdict": "UNVERIFIED", "confidence": 0}

    top = facts[0]
    score = top["score"]

    if score >= DECISION_THRESHOLD_HIGH:
        verdict = "SUPPORTED"
    elif score >= DECISION_THRESHOLD_LOW:
        verdict = "UNCERTAIN"
    else:
        verdict = "CONTRADICTED"

    return {
        "verdict": verdict,
        "confidence": round(score, 2),
        "fact_id": top["id"]
    }