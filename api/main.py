from fastapi import FastAPI
from pydantic import BaseModel
import requests

from orchestrator.pipeline_manager import run_pipeline

app = FastAPI()

# 🔹 Request model
class QueryRequest(BaseModel):
    query: str

# 🔹 ScaleDown API config
SCALEDOWN_API_URL = "https://api.scaledown.xyz/compress/raw/"
API_KEY = "GtDtKwAfQj1G4gYddY3ko4lVbAbkvmkl3i0sWLvW"   # 🔥 Replace with your real API key


# 🔹 Home route (test server)
@app.get("/")
def home():
    return {"status": "running"}


# 🔹 Main fact-check route
@app.post("/check")
def check_fact(request: QueryRequest):

    # 🔥 Step 1: Call ScaleDown API
    try:
        headers={
                "x-api-key": API_KEY,
                "Content-Type": "application/json"
            }
        response = requests.post(
            SCALEDOWN_API_URL,
            headers=headers,
            json={
                "model": "gpt-4o",
                "prompt": request.query
            },
           
        )
        print("STATUS CODE:",response.status_code)
        print("RAW API RESPONSE :",response.text)
        
        api_data = response.json()
        print("PARSED API DATA:",api_data)

    

    except Exception as e:
        return {"error": f"ScaleDown API failed: {str(e)}"}


    # 🔥 Step 2: Convert API output → facts (fallback logic)
    facts = []

    if not api_data or "error" in str(api_data).lower():
        facts = [
            {
                "id": 1,
                "similarity": 0.7,
                "credibility": 0.8,
                "timestamp": "2024-01-01"
            }
        ]
    else:
        # If API works, still create minimal usable structure
        facts = [
            {
                "id": 1,
                "similarity": 0.6,
                "credibility": 0.6,
                "timestamp": "2024-01-01"
            }
        ]


    # 🔥 Step 3: Run your reasoning pipeline
    result = run_pipeline(request.query, facts)


    # 🔹 Final response
    return {
        "query": request.query,
        "result": result
    }