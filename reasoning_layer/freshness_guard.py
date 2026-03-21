from datetime import datetime

def check_freshness(fact):
    today = datetime.now()
    fact_date = datetime.strptime(fact["timestamp"], "%Y-%m-%d")

    days_old = (today - fact_date).days

    # simple freshness score
    score = max(0, 1 - (days_old / 365))

    fact["freshness"] = score
    return fact