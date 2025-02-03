from .base_thinker import BaseThinker

class GPT4Thinker(BaseThinker):
    """GPT Thinker implementation."""
    
    def __init__(self, api_key: str, max_rounds: int = BaseThinker.DEFAULT_ROUNDS):
        super().__init__(name="GPT-4", api_key=api_key, max_rounds=max_rounds)
        self.model = "openai/o1"  # Updated to o1 model
        
    async def think(self, prompt: str) -> str:
        """Generate thoughts using GPT."""
        self.add_to_history("user", prompt)
        messages = [{"role": msg.role, "content": msg.content} 
                   for msg in self.conversation_history]
        
        response = await self._make_request(messages)
        self.add_to_history("assistant", response)
        return response 