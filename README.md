# Religion One Thinking

A Python-based AI religious thinking project that facilitates philosophical discussions between multiple AI models.

## Overview

Religion One Thinking creates a dialogue between different AI models (Gemini, GPT, DeepSeek) to explore philosophical and religious concepts. Each AI model contributes its unique perspective in a structured, progressive conversation.

## Features

- Multi-model AI dialogue system
- Real-time visualization dashboard
- Conversation export in Markdown format
- Progressive discussion framework
- Error handling and retry mechanisms

## Prerequisites

- Python 3.10
- Poetry (Python package manager)
- OpenRouter API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/wenqingyu/religion-one.git
cd religion-one
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Create a `.env` file in the project root:
```env
OPENROUTER_KEY=your_openrouter_api_key_here
```

## Running the Project

1. Start the thinking process:
```bash
poetry run religion-one
```

2. Start the visualization server:
```bash
poetry run religion-one-viz
```

3. Access the dashboard:
- Main dashboard: http://localhost:8000
- Conversation view: http://localhost:8000/conversation

## Project Structure

```
religion-one/
├── src/religion_one_thinking/
│   ├── thinkers/           # AI model implementations
│   │   ├── base_thinker.py
│   │   ├── gemini_thinker.py
│   │   ├── gpt4o_thinker.py
│   │   └── deepseek_thinker.py
│   ├── visualization/      # Web interface
│   │   ├── app.py
│   │   ├── run_server.py
│   │   └── templates/
│   └── main.py            # Main entry point
├── logs/                  # Conversation logs
├── tests/                # Test suite
└── pyproject.toml        # Project configuration
```

## Development Guide

### Adding a New AI Model

1. Create a new thinker class in `thinkers/`:
```python
from .base_thinker import BaseThinker

class NewThinker(BaseThinker):
    def __init__(self, api_key: str, max_rounds: int = BaseThinker.DEFAULT_ROUNDS):
        super().__init__(name="New-Model", api_key=api_key, max_rounds=max_rounds)
        self.model = "provider/model-name"
    
    async def think(self, prompt: str) -> str:
        self.add_to_history("user", prompt)
        messages = [{"role": msg.role, "content": msg.content} 
                   for msg in self.conversation_history]
        
        response = await self._make_request(messages)
        self.add_to_history("assistant", response)
        return response
```

2. Register the new thinker in `main.py`

### Modifying the Visualization

1. Templates are in `visualization/templates/`
2. Static files go in `visualization/static/`
3. Update routes in `visualization/app.py`

### Running Tests

```bash
poetry run pytest
```

## Future Development

Potential areas for improvement:

1. Enhanced Dialogue System
   - Better context management
   - Topic tracking
   - Argument analysis

2. Visualization Features
   - Real-time updates using WebSocket
   - Interactive conversation flow
   - Advanced data visualization

3. Model Integration
   - Support for more AI models
   - Model comparison metrics
   - Custom model configurations

4. Analysis Tools
   - Conversation sentiment analysis
   - Topic clustering
   - Argument mapping

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License

## Contact

Wenqing Yu - thomas.yu@knn3.xyz 