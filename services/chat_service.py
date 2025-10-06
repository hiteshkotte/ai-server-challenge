"""
Chat completion service - handles OpenAI and OpenRouter API calls
"""

from openai import OpenAI
from models import ChatCompletionRequest


class ChatService:
    def __init__(self, openai_key: str, openrouter_key: str):
        self.openai_client = OpenAI(api_key=openai_key)
        self.openrouter_client = OpenAI(
            api_key=openrouter_key,
            base_url="https://openrouter.ai/api/v1"
        )
    
    def complete(self, request: ChatCompletionRequest) -> dict:
        """
        Send chat completion request to appropriate provider
        
        Routes to OpenRouter if model name contains '/' (e.g., deepseek/deepseek-r1-0528:free)
        Otherwise routes to OpenAI
        """
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        params = {
            "model": request.model,
            "messages": messages,
        }
        
        if request.max_completion_tokens is not None:
            params["max_completion_tokens"] = request.max_completion_tokens
        
        # Route based on model name - OpenRouter models contain '/'
        if '/' in request.model:
            client = self.openrouter_client
        else:
            client = self.openai_client
        
        response = client.chat.completions.create(**params)
        return response.model_dump()