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
    print("\n--- New Lead Received ---")
    print(f"Name:    {lead.name}")
    print(f"Email:   {lead.email}")
    print(f"Message: {lead.message}")
    print("-------------------------\n")

    data = {
        "name": lead.name,
        "email": lead.email,
        "message": lead.message,
        "ai_summary": "Interested customer"
    }

    try:
        response = requests.post(
            APPS_SCRIPT_URL,
            headers={"Content-Type": "application/json"},
            json=data,
            timeout=15
        )

        print("Google status:", response.status_code)
        print("Google response:", response.text)

        return {
            "status": "success",
            "message": "Lead captured successfully!",
            "google_status": response.status_code,
            "google_response": response.text
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            "status": "error",
            "message": str(e)
        }
