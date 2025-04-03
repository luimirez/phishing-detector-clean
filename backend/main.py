import sys
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Fix import path for Render
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))
from app.detector import load_model

# FastAPI app instance
app = FastAPI(
    title="Phishing Awareness Detector API",
    description="API for detecting Phishing messages using a trained ML model",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class EmailScanRequest(BaseModel):
    content: str

# Root route
@app.get("/")
def read_root():
    return {"message": "Phishing awareness detector is running."}

# /scan route
@app.post("/scan")
async def scan_email(request: EmailScanRequest):
    model = load_model()
    if model is None:
        raise HTTPException(status_code=500, detail="Model not available.")

    prediction = model.predict([request.content])[0]
    return {"is_phishing": bool(prediction)}
