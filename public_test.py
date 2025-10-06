"""Simple public test for candidate to run"""

import json
import requests

SERVER_URL = "http://localhost:8090"


def test_chat_completions():
    """Test OpenAI proxy endpoint"""
    url = f"{SERVER_URL}/v1/chat/completions"
    payload = {
        "model": "gpt-5-mini",
        "messages": [{"role": "user", "content": "Hello, respond with just 'Hi!'"}],
        "max_completion_tokens": 10,
    }

    response = requests.post(url, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "choices" in data
    content = data["choices"][0]["message"]["content"].strip()
    print(f"✓ Chat completions: {content}")

def test_chat_completions_openrouter():
    """Test OpenRouter routing (may fail if free models are rate-limited)"""
    url = f"{SERVER_URL}/v1/chat/completions"
    payload = {
        "model": "google/gemini-2.0-flash-exp:free",
        "messages": [{"role": "user", "content": "Hi"}],
        "max_completion_tokens": 5,
    }

    response = requests.post(url, json=payload)
    # Accept both success and rate limit as valid responses
    # (proves routing works even if upstream is unavailable)
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.json()
        assert "choices" in data
        print("✓ OpenRouter routing: Success")
    else:
        # If 500, check it's an OpenRouter error (proves routing worked)
        error = response.json().get("detail", "")
        assert "openrouter" in error.lower() or "rate-limited" in error.lower()
        print("✓ OpenRouter routing: Connected (upstream rate-limited)")

def test_prefill_simple():
    """Test prefill endpoint with simple email"""
    url = f"{SERVER_URL}/v1/prefill"

    with open("emails/simple_invoice.txt", "r") as f:
        email_text = f.read()

    payload = {"email_text": email_text}
    response = requests.post(url, json=payload)

    assert response.status_code == 200
    data = response.json()
    print(f"✓ Prefill: {json.dumps(data, separators=(',', ':'))}")
    assert data["success"] is True

    # Show CSV
    import os
    import csv

    if os.path.exists("data.csv"):
        with open("data.csv", "r") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                print(f"Row {i + 1}: {json.dumps(dict(row), separators=(',', ':'))}")


def cleanup_csv():
    """Clean up CSV file after tests"""
    import os

    if os.path.exists("data.csv"):
        os.remove("data.csv")
        print("Cleaned up data.csv file")


if __name__ == "__main__":
    try:
        test_chat_completions()
        test_chat_completions_openrouter()
        test_prefill_simple()
        print("All tests passed!")
    finally:
        cleanup_csv()