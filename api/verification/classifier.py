def classify(query, retrieved_facts):
    if not retrieved_facts:
        return "UNVERIFIED"

    best_fact, score = retrieved_facts[0]

    if score > 0.75:
        return "TRUE"
    elif score > 0.5:
        return "PARTIALLY TRUE"
    else:
        return "FALSE"