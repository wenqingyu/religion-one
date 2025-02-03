import asyncio
from typing import List
from pathlib import Path
from ..thinkers.base_thinker import BaseThinker
from rich.console import Console

class DiscussionOrchestrator:
    def __init__(self, thinkers: List[BaseThinker]):
        self.thinkers = thinkers
        self.console = Console()
        
    async def load_thesis(self) -> str:
        thesis_path = Path("src/religion_one_thinking/thesis.txt")
        return thesis_path.read_text()
        
    async def load_description(self) -> str:
        desc_path = Path("src/religion_one_thinking/description.txt")
        return desc_path.read_text()
        
    async def conduct_discussion(self):
        thesis = await self.load_thesis()
        description = await self.load_description()
        
        # Initialize discussion with thesis and description
        for thinker in self.thinkers:
            self.console.print(f"[bold blue]{thinker.name} is thinking...[/]")
            response = await thinker.think(f"{description}\n\nThesis: {thesis}")
            self.console.print(f"[green]{thinker.name}[/]: {response}\n")
            
        # Continue discussion rounds
        round_num = 1
        while round_num <= 5:  # Or other termination condition
            self.console.print(f"\n[bold]Round {round_num}[/]")
            for thinker in self.thinkers:
                response = await thinker.think("Based on previous discussion, continue your thoughts.")
                self.console.print(f"[green]{thinker.name}[/]: {response}\n")
            round_num += 1 