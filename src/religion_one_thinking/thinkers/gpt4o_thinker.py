from .base_thinker import BaseThinker, Message
import httpx

class GPT4OThinker(BaseThinker):
    def __init__(self, api_key: str):
        super().__init__("GPT-4o Thinker", api_key)
        self.model = "openai/o1"
        
    async def think(self, prompt: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "HTTP-Referer": "http://localhost:8000",
                    "X-Title": "AI Religion Discussion"
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            return response.json()["choices"][0]["message"]["content"] 