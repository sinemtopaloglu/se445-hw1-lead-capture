from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from openai import OpenAI

app = FastAPI(title="Lead Capture API")

APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbw5USqy6yWf3M4PjRF4CMuTa6XOL7ZoK0apfFgihthbdcLm05RdigX0xjDVk_9iiN-d/exec"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Lead(BaseModel):
    name: str
    email: str
    message: str

def generate_ai_summary(message: str) -> str:
    response = client.responses.create(
        model="gpt-5",
        instructions="Summarize the user's lead message in one short professional sentence.",
        input=message
    )
    return response.output_text.strip()

@app.post("/lead")
async def capture_lead(lead: Lead):
    print("\n--- New Lead Received ---")
    print(f"Name:    {lead.name}")
    print(f"Email:   {lead.email}")
    print(f"Message: {lead.message}")
    print("-------------------------\n")

    try:
        ai_summary = generate_ai_summary(lead.message)
    except Exception as e:
        ai_summary = f"AI summary failed: {str(e)}"

    data = {
        "name": lead.name,
        "email": lead.email,
        "message": lead.message,
        "ai_summary": ai_summary
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
        print("AI Summary:", ai_summary)

        return {
            "status": "success",
            "message": "Lead captured successfully!",
            "ai_summary": ai_summary,
            "google_status": response.status_code,
            "google_response": response.text
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            "status": "error",
            "message": str(e)
        }
