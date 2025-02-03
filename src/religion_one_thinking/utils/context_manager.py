from typing import List, Dict
from datetime import datetime

class ConversationContext:
    """Manages the evolving context of the philosophical discussion."""
    
    def __init__(self):
        self.discussion_points = []
        self.key_themes = set()
        self.open_questions = []
        
    def add_contribution(self, thinker_name: str, content: str, round_num: int):
        """Add a new contribution to the discussion context."""
        timestamp = datetime.now().isoformat()
        
        contribution = {
            "thinker": thinker_name,
            "content": content,
            "round": round_num,
            "timestamp": timestamp
        }
        
        self.discussion_points.append(contribution)
        
    def get_context_prompt(self, current_round: int) -> str:
        """Generate a context-aware prompt for the next contribution."""
        if not self.discussion_points:
            return "Begin the philosophical discussion with your initial analysis."
            
        recent_points = self.discussion_points[-3:]  # Get last 3 contributions
        
        prompt = f"""Round {current_round} of the discussion.

Recent contributions:
{self._format_recent_points(recent_points)}

Based on these points:
1. What themes need further development?
2. What new perspectives can you add?
3. How can you help move the discussion forward?
4. What specific aspects should future responses address?

Provide your contribution that:
- Builds upon these previous insights
- Advances the key themes
- Proposes constructive next steps
- Helps move towards a deeper understanding

Your response should be both analytical and progressive, helping the discussion evolve."""
        
        return prompt
        
    def _format_recent_points(self, points: List[Dict]) -> str:
        """Format recent discussion points for context."""
        formatted = ""
        for point in points:
            formatted += f"\n{point['thinker']} (Round {point['round']}):\n"
            formatted += f"{self._summarize_content(point['content'])}\n"
        return formatted
        
    def _summarize_content(self, content: str, max_length: int = 200) -> str:
        """Create a brief summary of contribution content."""
        if len(content) <= max_length:
            return content
        return content[:max_length] + "..." 