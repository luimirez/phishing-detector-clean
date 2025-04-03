import os
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Ensure proper path resolution if needed
sys.path.append(os.path.dirname(__file__))
print("PYTHONPATH:", sys.path)

# Import from the correct module path
from backend.app.detector import load_model, is_phishing

# Create FastAPI instance
app = FastAPI(
    title="Phishing Awareness Detector API",
    description="API for detecting phishing messages using a trained ML model",
    version="1.0.0"
)

# Setup CORS (update allowed origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request schema
class EmailContent(BaseModel):
    subject: str
    body: str

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Phishing awareness detector is running."}

# Scan endpoint
@app.post("/scan")
async def scan_email(content: EmailContent):
    model = load_model()
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model not available.")
    
    # Combine subject and body for prediction
    combined_text = f"{content.subject} {content.body}"
    prediction = model.predict([combined_text])[0]
    
    return {"is_phishing": bool(prediction)}
