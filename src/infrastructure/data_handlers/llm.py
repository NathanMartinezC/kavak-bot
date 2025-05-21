import json
from openai import OpenAI
from src.infrastructure.config import settings

class LLMHandler:
    def __init__(
        self,
        api_key: str = settings.llm_api_key,
        base_url: str = settings.llm_api_url,
    ) -> None:
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
    def get_client(self):
        return self.client
    
    def make_request(
        self,
        prompt: str,
        max_tokens: int = 100,
        temperature: float = 0.2
    ):
        response = self.get_client().chat.completions.create(
            model=settings.llm_option,
            messages=[
                {"role": "user", "content": prompt}
            ],
            response_format={
                'type': 'json_object'
            },
            max_tokens=max_tokens,
            temperature=temperature,
        )
        
        return json.loads(response.choices[0].message.content)