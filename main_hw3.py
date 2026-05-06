from fastapi import FastAPI
from pydantic import BaseModel
import requests
import re
import os
import json
from openai import OpenAI

app = FastAPI(title="Lead Capture API - HW3")

APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycby0n4o-KXy80cO24U5pQGAmVBGek-R3iu1BgwQ7ijt9SoofU6wiAnDzacMoDMUxmDSiVw/exec"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class Lead(BaseModel):
    name: str = ""
    email: str = ""
    message: str = ""


def validate_lead(lead: Lead):
    errors = []

    if not lead.name.strip():
        errors.append("Missing name")

    if not lead.email.strip():
        errors.append("Missing email")
    else:
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.match(email_pattern, lead.email):
            errors.append("Invalid email format")

    if not lead.message.strip():
        errors.append("Missing message")

    if errors:
        return "Invalid", "; ".join(errors)

    return "Valid", "No validation errors"

def classify_lead(message: str):

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """
Classify the message intent and urgency.
Return only JSON.
"""
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            temperature=0
        )

    except Exception as e:
        print("AI ERROR:", e)

    text = message.lower()

    # Intent classification
    if (
        "price" in text
        or "pricing" in text
        or "buy" in text
        or "purchase" in text
        or "service" in text
    ):
        intent = "Sales"

    elif (
        "help" in text
        or "problem" in text
        or "issue" in text
        or "support" in text
    ):
        intent = "Support"

    elif (
        "partner" in text
        or "partnership" in text
        or "collaboration" in text
    ):
        intent = "Partnership"

    else:
        intent = "General"

    # Urgency classification
    if (
        "urgent" in text
        or "asap" in text
        or "immediately" in text
    ):
        urgency = "High"

    elif (
        "soon" in text
        or "quickly" in text
    ):
        urgency = "Medium"

    else:
        urgency = "Low"

    return intent, urgency

@app.post("/lead")
async def capture_lead(lead: Lead):

    validation_status, validation_notes = validate_lead(lead)

    if validation_status == "Valid":
        intent, urgency = classify_lead(lead.message)
    else:
        intent = "Not Classified"
        urgency = "Not Classified"

    data = {
        "name": lead.name,
        "email": lead.email,
        "message": lead.message,
        "validation_status": validation_status,
        "validation_notes": validation_notes,
        "intent": intent,
        "urgency": urgency
    }

    response = requests.post(
        APPS_SCRIPT_URL,
        headers={"Content-Type": "application/json"},
        json=data,
        timeout=15
    )

    return {
        "status": "success",
        "validation_status": validation_status,
        "validation_notes": validation_notes,
        "intent": intent,
        "urgency": urgency,
        "google_sheets_status": response.status_code
    }
