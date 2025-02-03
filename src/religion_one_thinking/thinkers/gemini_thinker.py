from .base_thinker import BaseThinker
import httpx

class GeminiThinker(BaseThinker):
    """Gemini 2.0 AI Thinker implementation using OpenRouter."""
    
    def __init__(self, api_key: str):
        """Initialize Gemini thinker with OpenRouter API key."""
        super().__init__(name="Gemini-2.0", api_key=api_key)
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "google/gemini-2.0-flash-thinking-exp-1219"
        
    async def think(self, prompt: str) -> str:
        """
        Generate thoughts using Gemini 2.0 via OpenRouter.
        
        Args:
            prompt: The input prompt to think about
            
        Returns:
            Generated response from Gemini
        """
        self.add_to_history("user", prompt)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://religion-one-thinking.com",  # Project domain
            "X-Title": "Religion One Thinking",  # Project name
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": msg.role, "content": msg.content}
                for msg in self.conversation_history
            ]
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.api_url,
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            response_text = result["choices"][0]["message"]["content"]
            
            self.add_to_history("assistant", response_text)
            return response_text

    @property
    def name(self) -> str:
        """Return the name of this thinker."""
        return "Gemini-2.0" 