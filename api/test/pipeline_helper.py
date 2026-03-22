from retrieval.retriever import (
    retrieve, add_fact, save_fact_to_file, load_facts
)

load_facts()

def add_user_fact(fact: str):
    add_fact(fact)            # add to memory
    save_fact_to_file(fact)   # save permanently