# Lead Capture API – SE445 HW1

## 📌 Overview

This project implements a simple lead capture system using FastAPI, Google Apps Script, and Google Sheets. The system collects user data (name, email, message), processes it, generates an AI summary, and stores the data in Google Sheets.

---

## ⚙️ Technologies Used

* FastAPI (Python)
* Uvicorn
* Google Apps Script
* Google Sheets
* JSON API

---

## 🔄 Workflow

1. User sends data via POST request to FastAPI endpoint (`/lead`)
2. FastAPI receives and processes the input
3. AI summary is generated from the message
4. Data is sent to Google Apps Script (webhook)
5. Data is stored in Google Sheets

---

## 🧠 Logic

The system receives user input (name, email, message), processes the data, generates an AI summary, and sends it to Google Sheets using a webhook integration.

---

## 🚀 API Endpoint

### POST /lead

### Example Request

```json
{
  "name": "Sinem Topaloğlu",
  "email": "sinemtopaloglu1907@gmail.com",
  "message": "I want to know your services"
}
```

---

## ✅ Output

* Data is successfully stored in Google Sheets
* AI summary is generated and saved
* API returns a success response

---

## 🧪 Testing

The API was tested using Swagger UI and successfully verified.

---

## 📷 Screenshots

* Swagger API test
* Terminal output
* Google Sheets data
* Apps Script deployment

(See report document for screenshots)

---

## 🎯 Result

The system successfully captures user data, processes it, and stores it in Google Sheets through a complete workflow.

---
