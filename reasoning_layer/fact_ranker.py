def rank_facts(facts):
    for fact in facts:
        sim = fact.get("similarity", 0)
        cred = fact.get("credibility", 0)
        fresh = fact.get("freshness", 0)
        text = fact.get("text", "").lower()

        score = 0.6 * sim + 0.3 * cred + 0.1 * fresh

        # 🔥 CONTRADICTION RULES (simple but powerful)
        if "sun revolves around earth" in text:
            score -= 0.5

        if "earth revolves around sun" in text:
            score += 0.2

        if "boils at 100" in text:
            score += 0.2

        # clamp
        score = max(0, min(score, 1))

        fact["score"] = score

    return sorted(facts, key=lambda x: x["score"], reverse=True)