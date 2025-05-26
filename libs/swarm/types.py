from typing import List, Callable, Union, Optional, TypedDict

AgentFunction = Callable[[], Union[str, "Agent", dict[str, str]]]


class Agent(TypedDict):
    name: str
    model: str
    instructions: Union[str, Callable[[], str]]
    functions: Optional[List[AgentFunction]]
    tool_choice: Optional[str]
    parallel_tool_calls: Optional[bool]


class Response(TypedDict):
    messages: list[str]
    agent: Optional[Agent]
    context_variables: dict[str, str]


class Result(TypedDict):
    """
    Encapsulates the possible return values for an agent function.

    Attributes:
        value (str): The result value as a string.
        agent (Agent): The agent instance, if applicable.
        context_variables (dict): A dictionary of context variables.
    """

    value: str
    agent: Optional[Agent]
    context_variables: dict[str, str]
