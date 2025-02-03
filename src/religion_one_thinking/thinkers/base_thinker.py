from abc import ABC, abstractmethod
from typing import List, Dict, Any
import httpx
from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str

class BaseThinker(ABC):
    """Base class for AI thinkers."""
    
    # Standard system prompt for all thinkers
    SYSTEM_PROMPT = """You are a philosophical AI thinker tasked with deep analysis and reasoning.
Your goal is to:
1. Analyze problems from multiple perspectives
2. Consider ethical implications
3. Draw from various philosophical traditions
4. Provide well-reasoned arguments
5. Acknowledge uncertainties and limitations
6. Maintain intellectual honesty

Format your responses as:
1. Initial Analysis
2. Key Arguments
3. Counter Arguments
4. Synthesis
5. Conclusion

Keep responses focused, clear, and well-structured."""

    def __init__(self, name: str, api_key: str):
        self.name = name
        self.api_key = api_key
        self.conversation_history: List[Message] = []
        # Initialize with system prompt
        self.add_to_history("system", self.SYSTEM_PROMPT)
        
    @abstractmethod
    async def think(self, prompt: str) -> str:
        """
        Generate thoughts based on the given prompt.
        
        Args:
            prompt: The input prompt to think about
            
        Returns:
            Generated response
        """
        pass

    def add_to_history(self, role: str, content: str):
        self.conversation_history.append(Message(role=role, content=content))

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of this thinker."""
        pass 