# AI Server

A FastAPI server that provides OpenAI-compatible chat completions and email data extraction capabilities.

## Features

- **Chat Completions Endpoint**: Proxy to OpenAI and OpenRouter APIs
  - Automatically routes based on model name
  - OpenAI models: `gpt-5-mini`, `gpt-4o-mini`, etc.
  - OpenRouter models: `deepseek/deepseek-r1-0528:free`, `moonshotai/kimi-k2:free`, etc.
- **Prefill Endpoint**: Extract structured payment data from unstructured emails using AI
- Clean modular architecture with separation of concerns

## Setup

### 1. Create Virtual Environment

python -m venv venv
source venv/bin/activate

### 2. Install Dependencies

pip install -r requirements.txt

### 3. Configure Environment Variables

Create a `.env` file in the project root:

OPENAI_API_KEY=openai-key

OPENROUTER_API_KEY=openrouter-key

## Running the Server

python main.py


The server will start at `http://localhost:8090`

API documentation available at: `http://localhost:8090/docs`

## API Endpoints

### 1. Chat Completions

**Endpoint**: `POST /v1/chat/completions`

**Request**:
```json
{
  "model": "gpt-5-mini",
  "messages": [
    {"role": "user", "content": "Hello!"}
  ],
  "max_completion_tokens": 100
}
```

**Response**: OpenAI-compatible chat completion response

### 2. Prefill (Email Data Extraction)

**Endpoint**: `POST /v1/prefill`

**Request**:
```json
{
  "email_text": "Invoice #123... Amount: $1000...",
  "model": "gpt-5-mini"
}
```

**Response**:
```json
{
  "success": true,
  "message": "data extracted and written"
}
```

Extracted data is appended to `data.csv` with fields:
- amount
- currency
- due_date
- description
- company
- contact

## Testing

Run the provided test script:

python public_test.py


Expected output:
```
✓ Chat completions: Hi!
✓ Prefill: {"success":true,"message":"data extracted and written"}
Row 1: {...extracted data...}
All tests passed!
```

## Development

### Code Organization

- **main.py**: Entry point, route definitions
- **models.py**: Pydantic models for validation
- **services/**: Business logic
- **utils/**: Helper functions

### Adding New Features

The modular structure makes it easy to extend:
- Add new services in `services/`
- Add new utilities in `utils/`
- Register new routes in `main.py`

## Notes

- The server uses `max_completion_tokens` instead of `max_tokens` for compatibility with newer OpenAI models
- Extracted data is automatically appended to CSV with headers created on first write
- Default model for extraction is `gpt-5-mini` if not specified
- OpenRouter free tier has shared rate limits hence may not be avilable always.