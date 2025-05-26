import inspect
from typing import Callable, Any


def function_to_json(func: Callable[..., Any]) -> dict[str, Any]:
    """
    Converts a Python function into a JSON-serializable dictionary
    that describes the function's signature, including its name,
    description, and parameters.

    Args:
        func: The function to be converted.

    Returns:
        A dictionary representing the function's signature in JSON format.
    """
    type_map: dict[type, str] = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
        type(None): "null",
    }

    try:
        signature = inspect.signature(func)
    except ValueError as e:
        raise ValueError(
            f"Failed to get signature for function {func.__name__}: {str(e)}"
        )

    parameters = {}
    for param in signature.parameters.values():
        param_type = type_map.get(param.annotation, "string")
        parameters[param.name] = {"type": param_type}

    required = [
        param.name
        for param in signature.parameters.values()
        if param.default == inspect.Parameter.empty
    ]

    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": func.__doc__ or "",
            "parameters": {
                "type": "object",
                "properties": parameters,
                "required": required,
            },
        },
    }


def jinja2_formatter(template: str, /, **kwargs: Any) -> str:
    """
    Formats a Jinja2 template string with the provided keyword arguments.

    Args:
        template (str): The Jinja2 template string to format.
        **kwargs: Keyword arguments to use for formatting the template.

    Returns:
        str: The formatted string.
    """
    try:
        from jinja2.sandbox import SandboxedEnvironment  # type: ignore
    except ImportError:
        raise ImportError("jinja2 is required for template formatting")

    env = SandboxedEnvironment()  # type: ignore
    return env.from_string(template).render(**kwargs)  # type: ignore
