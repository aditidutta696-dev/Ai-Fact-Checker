from api.retrieval.retriever import retrieve
from orchestrator.pipeline_manager import run_pipeline


# 🔹 STEP 1: Split claims
def split_into_claims(text: str):
    import re

    if not text:
        return []

    sentences = re.split(r'[.!?]+', text)
    claims = []

    for sentence in sentences:
        parts = re.split(r'\band\b|\bbut\b|\bor\b', sentence, flags=re.IGNORECASE)
        for part in parts:
            clean = part.strip()
            if clean:
                claims.append(clean)

    return claims


# 🔹 STEP 2: word set
def get_words(text: str):
    return set(text.lower().replace(".", "").split())


# 🔹 STEP 3: evaluate claim (FINAL LOGIC)
def evaluate_claim(claim: str):

    print("\n==============================")
    print("🔍 CLAIM:", claim)

    # 🔹 STEP 1: Retrieve
    retrieved = retrieve(claim)

    print("📦 Retrieved Results:", retrieved)

    if not retrieved:
        print("❌ No facts retrieved")
        return {
            "claim": claim,
            "verdict": "UNVERIFIED",
            "confidence": 0,
            "matched_fact": None
        }

    claim_words = set(claim.lower().split())
    print("🧠 Claim Words:", claim_words)

    best_match = None
    best_score = 0

    for fact, sim in retrieved:
        print("\n➡️ Checking Fact:", fact)

        fact_words = set(fact.lower().split())
        common = claim_words.intersection(fact_words)

        print("   Fact Words:", fact_words)
        print("   Common Words:", common)

        if len(claim_words) > 0:
            score = len(common) / len(claim_words)
        else:
            score = 0

        print("   Overlap Score:", score)

        if score > best_score:
            best_score = score
            best_match = fact

    print("\n✅ BEST MATCH:", best_match)
    print("⭐ BEST SCORE:", best_score)

    # Simple verdict
    if best_score >= 0.7:
        verdict = "SUPPORTED"
    elif best_score >= 0.4:
        verdict = "PARTIALLY_SUPPORTED"
    elif best_score >= 0.2:
        verdict = "UNCERTAIN"
    else:
        verdict = "REFUTED"

    return {
        "claim": claim,
        "verdict": verdict,
        "confidence": round(best_score, 2),
        "matched_fact": best_match
    }
# 🔹 STEP 4: main
def process_claim(query: str):

    if not query or not query.strip():
        return {
            "original_query": query,
            "processed_query": "",
            "result": {
                "overall_verdict": "UNVERIFIED",
                "confidence": 0,
                "details": []
            }
        }

    claims = split_into_claims(query)

    results = []
    scores = []

    for claim in claims:
        res = evaluate_claim(claim)
        results.append(res)
        scores.append(res["confidence"])

    avg_score = sum(scores) / len(scores) if scores else 0

    supported = sum(1 for r in results if r["verdict"] == "SUPPORTED")
    partial = sum(1 for r in results if r["verdict"] == "PARTIALLY_SUPPORTED")

    # 🔥 FINAL OVERALL LOGIC
    if supported == len(results):
        overall = "SUPPORTED"
    elif supported + partial >= len(results) / 2:
        overall = "PARTIALLY_SUPPORTED"
    elif avg_score >= 0.3:
        overall = "UNCERTAIN"
    else:
        overall = "REFUTED"

    return {
        "original_query": query,
        "processed_query": " | ".join(claims),
        "result": {
            "overall_verdict": overall,
            "confidence": round(avg_score, 2),
            "details": results
        }
    }


# 🔹 STEP 5: add fact
def add_user_fact(fact: str):
    try:
        from api.retrieval.retriever import add_fact, save_fact_to_file

        add_fact(fact)
        save_fact_to_file(fact)

        return {"status": "success"}

    except Exception as e:
        return {"status": "error", "message": str(e)}