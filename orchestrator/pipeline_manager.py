from reasoning_layer.freshness_guard import check_freshness
from reasoning_layer.conflict_resolver import resolve_conflicts
from reasoning_layer.fact_ranker import rank_facts
from reasoning_layer.decision_engine import make_decision

from performance_layer.cache_manager import get, set


def run_pipeline(query, facts):

    cached = get(query)
    if cached:
        return cached

    # Step 1: freshness
    facts = [check_freshness(f) for f in facts]

    # Step 2: conflict resolution
    facts = resolve_conflicts(facts)

    # Step 3: ranking
    facts = rank_facts(facts)

    # Step 4: decision
    result = make_decision(facts)

    set(query, result)

    return result