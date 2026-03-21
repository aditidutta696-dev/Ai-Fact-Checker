def resolve_conflicts(facts):
    if not facts:
        return []

    # sort by credibility + freshness
    return sorted(
        facts,
        key=lambda x: (x["credibility"], x.get("freshness", 0)),
        reverse=True
    )