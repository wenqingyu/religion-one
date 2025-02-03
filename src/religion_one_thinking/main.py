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
from .utils.context_manager import ConversationContext

class ReligionOneThinking:
    """Main class for the Religion One Thinking project."""
    
    def __init__(self, max_rounds: int = BaseThinker.DEFAULT_ROUNDS):
        load_dotenv()
        self.logger = ConversationLogger()
        self.context = ConversationContext()
        self.max_rounds = max_rounds
        self.thinkers: List[BaseThinker] = []
        self._initialize_thinkers()
        self._load_thesis()
        
    def _initialize_thinkers(self):
        """Initialize all AI thinkers."""
        openrouter_key = os.getenv("OPENROUTER_KEY")
        
        self.thinkers = [
            GeminiThinker(api_key=openrouter_key, max_rounds=self.max_rounds),
            GPT4Thinker(api_key=openrouter_key, max_rounds=self.max_rounds),
            DeepSeekThinker(api_key=openrouter_key, max_rounds=self.max_rounds)
        ]
        
    def _load_thesis(self) -> str:
        """Load the main thesis question."""
        thesis_path = Path(__file__).parent / "thesis.txt"
        with open(thesis_path, "r", encoding="utf-8") as f:
            self.thesis = f.read().strip()
            
    async def think(self):
        """Have all thinkers contemplate the thesis."""
        round_number = 1
        consecutive_errors = 0  # Track consecutive errors
        max_consecutive_errors = 3  # Maximum allowed consecutive errors
        
        while round_number <= self.max_rounds:
            print(f"\n=== Round {round_number} ===\n")
            
            for thinker in self.thinkers:
                try:
                    # Get context-aware prompt
                    context_prompt = self.context.get_context_prompt(round_number)
                    full_prompt = f"{self.thesis}\n\n{context_prompt}"
                    
                    response = await thinker.think(full_prompt)
                    consecutive_errors = 0  # Reset error counter on success
                    
                    # Add to context
                    self.context.add_contribution(thinker.name, response, round_number)
                    
                    self.logger.log_conversation(
                        thinker_name=thinker.name,
                        prompt=full_prompt,
                        response=response,
                        metadata={
                            "round": round_number,
                            "model": thinker.model,
                            "conversation_history": [
                                {"role": msg.role, "content": msg.content}
                                for msg in thinker.conversation_history
                            ]
                        }
                    )
                    print(f"\n=== {thinker.name}'s Response (Round {round_number}) ===\n")
                    print(response)
                    
                except Exception as e:
                    consecutive_errors += 1
                    error_msg = str(e)
                    
                    self.logger.log_conversation(
                        thinker_name=thinker.name,
                        prompt=full_prompt,
                        error=error_msg,
                        metadata={
                            "round": round_number,
                            "model": thinker.model,
                            "error_type": e.__class__.__name__
                        }
                    )
                    print(f"Error with {thinker.name}: {error_msg}")
                    
                    # Stop if too many consecutive errors
                    if consecutive_errors >= max_consecutive_errors:
                        print("\nToo many consecutive errors. Stopping execution.")
                        return
                
                print("\n" + "="*50 + "\n")
                await asyncio.sleep(1)  # Add delay between requests
            
            round_number += 1

def main():
    """Entry point for the CLI."""
    asyncio.run(async_main())

async def async_main():
    project = ReligionOneThinking()
    await project.think()

if __name__ == "__main__":
    main() 