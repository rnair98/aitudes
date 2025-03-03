from typing import List, Callable, Union, Optional, TypedDict

AgentFunction = Callable[[], Union[str, "Agent", dict]]


class Agent(TypedDict):
    name: str = "Agent"
    model: str = "gpt-4o"
    instructions: Union[str, Callable[[], str]] = "You are a helpful agent."
    functions: List[AgentFunction] = []
    tool_choice: str = None
    parallel_tool_calls: bool = True


class Response(TypedDict):
    messages: List = []
    agent: Optional[Agent] = None
    context_variables: dict = {}


class Result(TypedDict):
    """
    Encapsulates the possible return values for an agent function.

    Attributes:
        value (str): The result value as a string.
        agent (Agent): The agent instance, if applicable.
        context_variables (dict): A dictionary of context variables.
    """

    value: str = ""
    agent: Optional[Agent] = None
    context_variables: dict = {}
