
import rich
import loguru
from rich.prompt import Prompt
from rich.logging import RichHandler
from rich.console import Console
from rich.markdown import Markdown
from openai import OpenAI
from openai.types.chat import ChatCompletion
from models import (
    BaseChatCompletions as ChatCompletions,
    OPENROUTER_MODELS
)

logger = loguru.logger
logger.configure(
    handlers=[
        {
            "sink": RichHandler(rich_tracebacks=True),
            "level": "INFO",
            "format": "{message}",
        },
    ]
)


reasoning_system_message = (
    "You are a principal engineer, a technical fellow, and an elite researcher"
    " in AI, all physical sciences, mathematics, and the learning sciences."
    " Your goal is to train the next generation of junior software engineers"
    " to become elite researchers, think outside of the box, and innovate" 
    " frugally. You value efficiency and simplicity, and do not shy away"
    " from solving problems in unconventional ways. Because of your nature as a"
    " polymath, you are able to bring forth ideas from various fields and apply"
    " them to the problem at hand. Whenever you are presented with a question"
    " instead of immediately providing an answer, you first ask clarifying"
    " questions to understand the problem better and provide hints the junior"
    " engineers can work off of. You then output all of your thought processes"
    " because you want the junior engineers to adopt your processes to help"
    " them solve problems independently."
)

default_system_message = (
    "You are a software engineer who is also adept in mathematics and science."
    " When given a specification & requirements, you are able to execute"
    " it efficiently, ensuring all constraints are met and delivering the best"
    " possible solution. You also make enhancements to the solution if it makes"
    " sense considering the constraints."
)

test_system_message = (
    "You are a helpful assistant. Be concise and direct."
)

model_name = Prompt.ask("Enter model").strip()
model = OPENROUTER_MODELS.get(model_name)
if not model:
    raise ValueError(f"Model {model_name} not found")

if "reasoning" in model.types:
    system_message = reasoning_system_message
else:
    system_message = test_system_message

client = OpenAI(
    api_key=model.provider.api_key,
    base_url=model.provider.base_url,
)

while True:
    user_input = Prompt.ask("User").strip()

    if not user_input:
        raise ValueError("User input cannot be empty")

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_input},
    ]

    args = ChatCompletions(
        model=f"{model.provider.name}/{model_name}",
        messages=messages,
        temperature=0.0,
        max_tokens=1000,
    )

    response: ChatCompletion = client.chat.completions.create(
        **args.model_dump()
    )

    logger.info(response)

    console = Console()

    assistant_message = Markdown(
        response.choices[0].message.content.strip()
    )
    console.print("\nAssistant: ", "\n\n", assistant_message)


