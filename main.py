"""
AI Server - FastAPI application

Entry point for the server. Provides two main endpoints:
1. /v1/chat/completions - OpenAI-compatible chat proxy
2. /v1/prefill - Email data extraction to CSV
"""

import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import uvicorn

from models import ChatCompletionRequest, PrefillRequest, PrefillResponse
from services.chat_service import ChatService
from services.extraction_service import ExtractionService
from utils.csv_handler import CSVHandler

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(title="AI Server", version="1.0.0")

# Initialize services
chat_service = ChatService(
    openai_key=os.getenv("OPENAI_API_KEY"),
    openrouter_key=os.getenv("OPENROUTER_API_KEY")
)
extraction_service = ExtractionService(api_key=os.getenv("OPENAI_API_KEY"))

# CSV configuration
CSV_FILE = "data.csv"
CSV_HEADERS = ["amount", "currency", "due_date", "description", "company", "contact"]
csv_handler = CSVHandler(CSV_FILE, CSV_HEADERS)


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """
    OpenAI-compatible chat completions endpoint
    Proxies requests to OpenAI API
    """
    try:
        return chat_service.complete(request)
    except Exception as e:
        print(f"Chat completion error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/prefill", response_model=PrefillResponse)
async def prefill(request: PrefillRequest):
    """
    Extract payment information from email text and save to CSV
    Uses AI to parse unstructured email into structured data
    """
    try:
        if not request.email_text or not request.email_text.strip():
            return PrefillResponse(success=False, message="email_text cannot be empty")
        
        # Default to gpt-5-mini if no model specified
        model = request.model if request.model else "gpt-5-mini"
        
        # Extract data and write to CSV
        extracted_data = extraction_service.extract_payment_info(request.email_text, model)
        csv_handler.append(extracted_data)
        
        return PrefillResponse(success=True, message="data extracted and written")
    
    except Exception as e:
        print(f"Prefill error: {str(e)}")
        return PrefillResponse(success=False, message=f"something went wrong: {str(e)}")


if __name__ == "__main__":
    print("Starting AI Server on http://localhost:8090")
    print("API Docs available at http://localhost:8090/docs")
    
    uvicorn.run(app, host="localhost", port=8090, log_level="info")