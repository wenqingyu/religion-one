from .base_thinker import BaseThinker

class GeminiThinker(BaseThinker):
    """Gemini AI Thinker implementation."""
    
    def __init__(self, api_key: str, max_rounds: int = BaseThinker.DEFAULT_ROUNDS):
        super().__init__(name="Gemini-1.5", api_key=api_key, max_rounds=max_rounds)
        self.model = "google/gemini-pro-1.5"
        
    async def think(self, prompt: str) -> str:
        """Generate thoughts using Gemini."""
        self.add_to_history("user", prompt)
        messages = [{"role": msg.role, "content": msg.content} 
                   for msg in self.conversation_history]
        
        response = await self._make_request(messages)
        self.add_to_history("assistant", response)
        return response

    @property
    def name(self) -> str:
        """Return the name of this thinker."""
        return "Gemini-2.0" 