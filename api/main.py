from fastapi import FastAPI
from pydantic import BaseModel
import requests

# 🔥 Use pipeline_helper instead of directly calling pipeline_manager
from api.test.pipeline_helper import process_claim, add_user_fact

app = FastAPI()


# 🔹 Request model
class QueryRequest(BaseModel):
    query: str


# 🔹 ScaleDown API config
SCALEDOWN_API_URL = "https://api.scaledown.xyz/compress/raw/"
API_KEY = "ASMVVB3o6f2MXMbOSqQ7B9UnRfMSTmo9I18Xet1g"   # 🔥 Put your real API key


# 🔹 Home route
@app.get("/")
def home():
    return {"status": "running"}


# 🔥 ScaleDown function (CLEAN + CORRECT)
def get_scaledown_text(query: str):
    try:
        headers = {
            "x-api-key": API_KEY,
            "Content-Type": "application/json"
        }

        response = requests.post(
            SCALEDOWN_API_URL,
            headers=headers,
            json={
                "model": "gpt-4o",
                "prompt": f"Simplify and clean this claim: {query}"
            }
        )

        print("STATUS CODE:", response.status_code)
        print("RAW RESPONSE:", response.text)

        data = response.json()

        # 🔥 Extract processed text safely
        return data.get("output", query)

    except Exception as e:
        print("ScaleDown error:", e)
        return query  # fallback


# 🔹 Main fact-check route
@app.post("/check")
def check_fact(request: QueryRequest):

    # 🔥 Step 1: Process query using ScaleDown
    processed_query = get_scaledown_text(request.query)

    print("Original Query:", request.query)
    print("Processed Query:", processed_query)

    # 🔥 Step 2: Use pipeline_helper (FULL SYSTEM)
    result = process_claim(processed_query)

    return {
        "original_query": request.query,
        "processed_query": processed_query,
        "result": result
    }


# 🔹 Add new fact route (connects ingestion)
@app.post("/add_fact")
def add_fact(request: QueryRequest):

    add_user_fact(request.query)

    return {
        "message": "Fact added successfully",
        "fact": request.query
    }