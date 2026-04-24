from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI(title="Lead Capture API")

APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbw5USqy6yWf3M4PjRF4CMuTa6XOL7ZoK0apfFgihthbdcLm05RdigX0xjDVk_9iiN-d/exec"

class Lead(BaseModel):
    name: str
    email: str
    message: str

@app.post("/lead")
async def capture_lead(lead: Lead):
    print("\n--- New HW2 Lead Received ---")
    print(f"Name: {lead.name}")
    print(f"Email: {lead.email}")
    print(f"Message: {lead.message}")
    print("-----------------------------\n")

    data = {
        "name": lead.name,
        "email": lead.email,
        "message": lead.message
    }

    try:
        response = requests.post(
            APPS_SCRIPT_URL,
            headers={"Content-Type": "application/json"},
            json=data,
            timeout=15
        )

        return {
            "status": "success",
            "message": "Lead stored successfully!",
            "google_status": response.status_code
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
