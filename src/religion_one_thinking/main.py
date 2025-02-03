import asyncio
from pathlib import Path
import os
from dotenv import load_dotenv
from typing import List

from .thinkers.base_thinker import BaseThinker
from .thinkers.gemini_thinker import GeminiThinker
from .thinkers.gpt4o_thinker import GPT4Thinker
from .thinkers.deepseek_thinker import DeepSeekThinker
from .utils.logger import ConversationLogger

class ReligionOneThinking:
    """Main class for the Religion One Thinking project."""
    
    def __init__(self):
        load_dotenv()
        self.logger = ConversationLogger()
        self.thinkers: List[BaseThinker] = []
        self._initialize_thinkers()
        self._load_thesis()
        
    def _initialize_thinkers(self):
        """Initialize all AI thinkers."""
        openrouter_key = os.getenv("OPENROUTER_KEY")
        
        self.thinkers = [
            GeminiThinker(api_key=openrouter_key),
            GPT4Thinker(api_key=openrouter_key),
            DeepSeekThinker(api_key=openrouter_key)
        ]
        
    def _load_thesis(self) -> str:
        """Load the main thesis question."""
        thesis_path = Path(__file__).parent / "thesis.txt"
        with open(thesis_path, "r", encoding="utf-8") as f:
            self.thesis = f.read().strip()
            
    async def think(self):
        """Have all thinkers contemplate the thesis."""
        for thinker in self.thinkers:
            try:
                response = await thinker.think(self.thesis)
                self.logger.log_conversation(
                    thinker_name=thinker.name,
                    prompt=self.thesis,
                    response=response,
                    metadata={
                        "model": thinker.model,
                        "conversation_history": [
                            {"role": msg.role, "content": msg.content}
                            for msg in thinker.conversation_history
                        ]
                    }
                )
                print(f"\n=== {thinker.name}'s Response ===\n")
                print(response)
                print("\n" + "="*50 + "\n")
                
            except Exception as e:
                print(f"Error with {thinker.name}: {str(e)}")

def main():
    """Entry point for the CLI."""
    asyncio.run(async_main())

async def async_main():
    project = ReligionOneThinking()
    await project.think()

if __name__ == "__main__":
    main() 