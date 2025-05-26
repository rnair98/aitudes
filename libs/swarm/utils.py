import inspect
from typing import Callable, Any


def function_to_json(func: Callable[..., Any]) -> dict[str, Any]:
    """
    Converts a Python function's signature into a JSON-serializable dictionary.
    
    The returned dictionary includes the function's name, docstring, and a schema describing its parameters and which are required. Parameter types are mapped to JSON schema types where possible.
    
    Args:
        func: The Python function to describe.
    
    Returns:
        A dictionary representing the function's signature and parameters in a JSON-compatible format.
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
    Renders a Jinja2 template string using the provided keyword arguments.
    
    Raises:
        ImportError: If the Jinja2 library is not installed.
    
    Returns:
        The rendered template as a string.
    """
    try:
        from jinja2.sandbox import SandboxedEnvironment  # type: ignore
    except ImportError as err:
        raise ImportError("jinja2 is required for template formatting") from err

    env = SandboxedEnvironment()  # type: ignore
    return env.from_string(template).render(**kwargs)  # type: ignore
