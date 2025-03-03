# Aitudes

Aitudes is a Python framework for interacting with various Large Language Models (LLMs) through a unified interface, with a focus on creating AI-powered agents.

## Features

- **Model Agnostic Interface**: Connect to multiple LLM providers including OpenAI, Google (Gemini), Perplexity, Mistral and more through OpenRouter
- **Agent Framework**: Flexible agent system with support for function calling
- **Multimodal Support**: Handle text, image, and audio inputs/outputs
- **Type System**: Well-defined types for agents, models, and interactions
- **Rich Console Interface**: Terminal-friendly interfaces using the Rich library
- **Progress Tracking**: Custom TQDM implementation for monitoring long-running tasks

## Installation

```bash
pip install -r requirements.txt
```

## Requirements

- Python 3.11+
- Dependencies defined in requirements.txt and pyproject.toml

## Usage

### Basic Example

```python
from libs.swarm import Agent

# Initialize an agent
agent = Agent(model="gpt-4")

# Chat with the agent
response = agent.chat("Tell me about artificial intelligence")
print(response)
```

### Function Calling

```python
from libs.swarm import Agent, define_function

# Define a function for the agent to call
@define_function
def get_weather(location: str, unit: str = "celsius"):
    """Get the weather for a location."""
    # Implementation
    return {"temperature": 22, "conditions": "sunny"}

# Initialize an agent with function calling
agent = Agent(model="gpt-4", functions=[get_weather])

# The agent can now use the get_weather function
result = agent.chat("What's the weather in Paris?")
```

## Project Structure

- `libs/swarm/`: Core functionality for LLM interactions and agent framework
- `utils/`: Helper utilities including progress tracking
- `notebooks/`: Example notebooks demonstrating usage

## License

See the [LICENSE](LICENSE) file for details.