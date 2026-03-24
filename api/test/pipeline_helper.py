#pipeline_helper.py
from orchestrator.pipeline_manager import run_pipeline
import re


# 🔹 STEP 1: Split paragraph into smaller claims
def split_into_claims(text: str):


    # 🔥 Split on conjunctions AND punctuation
    parts = re.split(r"\b(?:and|but|or|while)\b|[,.!?]+", text, flags=re.IGNORECASE)

    return [p.strip() for p in parts if p.strip()]

def detect_contradictions(claim: str, fact_texts):
    penalty = 0.0

    claim_lower = claim.lower()

    for fact in fact_texts:
        fact_lower = fact.lower()

        # 🔥 ONLY penalize if meaning truly conflicts
        if "not" in claim_lower and "not" not in fact_lower:
            # check strong mismatch instead of direct penalty
            if any(word in fact_lower for word in ["is", "are", "was"]):
                penalty += 0.1

        elif "not" not in claim_lower and "not" in fact_lower:
            if any(word in claim_lower for word in ["is", "are", "was"]):
                penalty += 0.1

    return min(penalty, 0.3)  # 🔥 reduce max penalty

# 🔹 STEP 2: Evaluate a single claim USING FULL PIPELINE
def evaluate_claim(claim: str):

    print("\n🔍 Checking Claim:", claim)

    result = run_pipeline(claim)

    facts = result.get("details", [])
    fact_texts = [f.get("text", "") for f in facts]

    penalty = detect_contradictions(claim, fact_texts)

    base_conf = result.get("confidence", 0)

    print("📊 Base Confidence:", base_conf)
    print("⚠️ Penalty:", penalty)

    # 🔥 NEGATION HANDLING (INLINE FIX - NO NEW FUNCTION)
    claim_lower = claim.lower()
    neg_words = [" not ", " no ", " never ", "does not", "do not"]

    claim_has_neg = any(w in claim_lower for w in neg_words)

    adjusted_conf = base_conf

    for fact in fact_texts:
        fact_lower = fact.lower()
        fact_has_neg = any(w in fact_lower for w in neg_words)

        # 🔥 If negation mismatch → reduce confidence
        if claim_has_neg != fact_has_neg:
            adjusted_conf -= 0.5

    # 🔥 final confidence after penalty
    final_conf = max(0, adjusted_conf - penalty)

    # 🔥 smarter verdict logic
    if final_conf > 0.7:
        verdict = "SUPPORTED"
    elif final_conf > 0.5:
        verdict = "PARTIALLY_SUPPORTED"
    elif final_conf > 0.3:
        verdict = "UNCERTAIN"
    else:
        verdict = "REFUTED"

    return {
        "claim": claim,
        "verdict": verdict,
        "confidence": round(final_conf, 2)
    }
# 🔹 MAIN FUNCTION
def process_claim(query: str):

    claims = split_into_claims(query)

    results = []
    scores = []

    for claim in claims:
        result = evaluate_claim(claim)
        results.append(result)
        scores.append(result["confidence"])

    # 🔹 overall decision
    avg_score = sum(scores) / len(scores) if scores else 0

    if avg_score > 0.75:
        overall = "SUPPORTED"
    elif avg_score > 0.5:
        overall = "PARTIALLY_SUPPORTED"
    elif avg_score > 0.3:
        overall = "UNCERTAIN"
    else:
        overall = "REFUTED"

    return {
        "result": {
            "overall_verdict": overall,
            "confidence": round(avg_score, 2),
            "details": results
        }
    }


# 🔹 ADD FACT (UNCHANGED)
def add_user_fact(fact: str):
    try:
        from api.retrieval.retriever import add_fact, save_fact_to_file

        add_fact(fact)
        save_fact_to_file(fact)

        return {
            "status": "success",
            "message": "Fact added successfully"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }