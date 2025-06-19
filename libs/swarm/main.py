import loguru
from rich.prompt import Prompt
from rich.logging import RichHandler
from rich.console import Console
from rich.markdown import Markdown
from openai import OpenAI
from openai.types.responses import Response
from models import OPENROUTER_MODELS, PROVIDER
from dotenv import load_dotenv


load_dotenv()


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
    "Always respond using the GitHub Flavored Markdown Spec with fenced code blocks."
)

system_message = (
    "You are a senior software engineer & AI researcher who is capable of using a combination"
    " of techniques and tools to solve problems efficiently and effectively."
    " When given a specification & requirements, you are able to execute"
    " it efficiently, ensuring all constraints are met and delivering the best"
    " possible solution. You also make enhancements to the solution if it makes"
    " sense considering the constraints. "
    "Always respond using the GitHub Flavored Markdown Spec with fenced code blocks."
)

model_name = Prompt.ask("Enter model").strip()
provider = Prompt.ask("Enter provider").strip()
if provider == PROVIDER.OPENROUTER:
    model = OPENROUTER_MODELS.get(model_name)
    if not model:
        raise ValueError(f"Model {model_name} not found")
    if model.types and "reasoning" in model.types:
        system_message = reasoning_system_message

    client = OpenAI(
        api_key=model.provider.api_key,
        base_url=model.provider.base_url,
    )
    model_name = f"{model.provider.name}/{model_name}"
else:
    client = OpenAI()

while True:
    user_input = Prompt.ask("User").strip()

    if not user_input:
        raise ValueError("User input cannot be empty")

    response: Response = client.responses.create(
        model=model_name, instructions=system_message, input=user_input
    )
    logger.info(response)

    console = Console()

    assistant_message = Markdown(response.output_text)
    console.print("\nAssistant: ", "\n\n", assistant_message)
