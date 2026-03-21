cache = {}

def get(query):
    return cache.get(query)

def set(query, result):
    cache[query] = result