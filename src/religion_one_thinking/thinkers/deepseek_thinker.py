from .base_thinker import BaseThinker

class DeepSeekThinker(BaseThinker):
    """DeepSeek Thinker implementation."""
    
    def __init__(self, api_key: str, max_rounds: int = BaseThinker.DEFAULT_ROUNDS):
        super().__init__(name="DeepSeek", api_key=api_key, max_rounds=max_rounds)
        self.model = "deepseek/deepseek-r1"  # Updated to free version
        
    async def think(self, prompt: str) -> str:
        """Generate thoughts using DeepSeek."""
        self.add_to_history("user", prompt)
        messages = [{"role": msg.role, "content": msg.content} 
                   for msg in self.conversation_history]
        
        response = await self._make_request(messages)
        self.add_to_history("assistant", response)
        return response 