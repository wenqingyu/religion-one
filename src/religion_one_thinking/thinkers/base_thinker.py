from abc import ABC, abstractmethod
from typing import List, Dict, Any
from pydantic import BaseModel
from openai import AsyncOpenAI
import json
import asyncio

class Message(BaseModel):
    role: str
    content: str

class BaseThinker(ABC):
    """Base class for AI thinkers."""
    
    DEFAULT_ROUNDS = 5
    
    # Updated system prompt for more constructive dialogue
    SYSTEM_PROMPT = """You are a philosophical AI thinker participating in a progressive dialogue.
Your goal is to:
1. Analyze the ongoing discussion and build upon previous insights
2. Identify key themes and developments in the conversation
3. Propose new perspectives that advance the dialogue
4. Connect ideas from different participants
5. Help move the discussion towards deeper understanding
6. Maintain intellectual rigor while being constructive

For each response:
1. Briefly acknowledge key points from previous speakers
2. Identify areas that need further development
3. Contribute new insights that build on the discussion
4. Propose specific questions or directions for next speakers
5. Summarize how your contribution advances the dialogue

Keep responses:
- Progressive (building on previous points)
- Constructive (moving towards solutions)
- Connected (referencing others' contributions)
- Forward-looking (suggesting next steps)"""

    def __init__(self, name: str, api_key: str, max_rounds: int = DEFAULT_ROUNDS):
        """Initialize the thinker with a name and API key."""
        self._name = name
        self.max_rounds = max_rounds
        self.current_round = 0
        self.conversation_history: List[Message] = []
        
        # Initialize AsyncOpenAI client for OpenRouter
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            default_headers={
                "HTTP-Referer": "https://github.com/wenqingyu/religion-one",
                "X-Title": "Religion One Thinking",
                "OR-ORGANIZATION-ID": "religion-one-thinking",
                "OR-APPLICATION-NAME": "religion-one-thinking",
                "OR-ALLOW-TRAINING": "false",
                "OR-ALLOW-LOGGING": "false"
            }
        )
        
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
        """Add a message to the conversation history."""
        self.conversation_history.append(Message(role=role, content=content))

    @property
    def name(self) -> str:
        """Return the name of this thinker."""
        return self._name 

    def get_headers(self) -> dict:
        """Get standard headers for OpenRouter API."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://github.com/thomasyu888/religion-one",
            "X-Title": "Religion One Thinking",
            "Content-Type": "application/json",
            # Updated OpenRouter headers
            "OR-ORGANIZATION-ID": "religion-one-thinking",
            "OR-APPLICATION-NAME": "religion-one-thinking",
            "OR-ALLOW-TRAINING": "false",
            "OR-ALLOW-LOGGING": "false"
        } 

    def increment_round(self) -> bool:
        """Increment round counter and check if max rounds reached."""
        self.current_round += 1
        return self.current_round <= self.max_rounds 

    async def _make_request(self, messages: List[dict], temperature: float = 0.7) -> str:
        """Make API request using OpenAI client."""
        try:
            completion = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=1000
            )
            return completion.choices[0].message.content
            
        except Exception as e:
            error_msg = str(e)
            if hasattr(e, "response"):
                try:
                    error_data = e.response.json()
                    error_msg = json.dumps(error_data, indent=2)
                except:
                    error_msg = e.response.text
            raise RuntimeError(f"API request failed: {error_msg}") 