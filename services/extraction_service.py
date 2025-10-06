"""
Email data extraction service - uses AI to extract structured data
"""

import json
import re
from typing import Dict
from openai import OpenAI


class ExtractionService:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.required_fields = ["amount", "currency", "due_date", "description", "company", "contact"]
    
    def extract_payment_info(self, email_text: str, model: str) -> Dict[str, str]:
        """
        Extract payment information from email text using AI
        
        Returns dict with required fields: amount, currency, due_date, 
        description, company, contact
        """
        prompt = self._build_prompt(email_text)
        response = self._call_ai(prompt, model)
        extracted = self._parse_response(response)
        
        return self._ensure_all_fields(extracted)
    
    def _build_prompt(self, email_text: str) -> str:
        """Create extraction prompt for AI"""
        return f"""Extract the following payment information from the email below.
Return ONLY a JSON object with these exact fields (use null if information is not found):
- amount (numeric value only, without currency symbol)
- currency (3-letter code like USD, EUR, etc.)
- due_date (format: YYYY-MM-DD)
- description (brief description of what the payment is for)
- company (company name issuing the invoice)
- contact (email or phone contact information)

Email text:
{email_text}

Return only valid JSON, no other text."""
    
    def _call_ai(self, prompt: str, model: str) -> str:
        """Call AI model for extraction"""
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a data extraction assistant. Extract information accurately and return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=500
        )
        content = response.choices[0].message.content
        
        if content is None:
            raise ValueError("AI returned None as content")
        
        return content.strip()
    
    def _parse_response(self, content: str) -> dict:
        """
        Parse AI response, handling markdown code blocks
        
        AI sometimes wraps JSON in ```json ... ``` blocks
        """
        if "```" in content:
            pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                content = match.group(1)
            else:
                content = content.replace("```json", "").replace("```", "").strip()
        
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            # Try to find JSON object in response
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', content, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    raise ValueError(f"Could not parse AI response as JSON: {str(e)}")
            else:
                raise ValueError("No JSON object found in AI response")
    
    def _ensure_all_fields(self, extracted: dict) -> Dict[str, str]:
        """Ensure all required fields are present, convert None to empty string"""
        result = {}
        for field in self.required_fields:
            value = extracted.get(field)
            result[field] = str(value) if value is not None and value != "null" else ""
        return result