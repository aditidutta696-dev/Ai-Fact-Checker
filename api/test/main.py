import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from api.test.pipeline_helper import process_claim, add_user_fact

while True:
    print("\n1. Check a claim")
    print("2. Add a new fact")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        claim = input("Enter claim: ")
        result = process_claim(claim)

        print("Verdict:", result["verdict"])

    elif choice == "2":
        fact = input("Enter new fact: ")
        add_user_fact(fact)
        print("✅ Fact added & saved!")

    elif choice == "3":
        break