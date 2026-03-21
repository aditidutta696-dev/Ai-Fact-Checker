def rank_facts(facts):
    for fact in facts:
        fact["score"] = (
            0.5 * fact.get("similarity", 0) +
            0.3 * fact.get("credibility", 0) +
            0.2 * fact.get("freshness", 0)
        )

    return sorted(facts, key=lambda x: x["score"], reverse=True)
