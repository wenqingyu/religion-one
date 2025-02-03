from datetime import datetime
import json
from pathlib import Path
from typing import Any, Dict

class ConversationLogger:
    """Logger for AI thinking conversations."""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
    def log_conversation(self, 
                        thinker_name: str, 
                        prompt: str, 
                        response: str,
                        metadata: Dict[str, Any] = None):
        """Log a conversation entry with metadata."""
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "thinker": thinker_name,
            "prompt": prompt,
            "response": response,
            "metadata": metadata or {}
        }
        
        # Create daily log file
        date_str = datetime.now().strftime("%Y-%m-%d")
        log_file = self.log_dir / f"conversation_log_{date_str}.jsonl"
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n") 