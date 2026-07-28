import inspect
import typing
from typing import Any, Callable, Dict, Optional

from gen_ai_hub.orchestration.models.base import JSONSerializable


def python_type_to_json_type(py_type):
    """Converts a Python type to a JSON Schema type.

    :param py_type: The Python type to convert.
    :type py_type: type
    :return: A dictionary representing the JSON Schema type.
    :rtype: Dict[str, Any]
    """
    origin = typing.get_origin(py_type)
    args = typing.get_args(py_type)

    # Simple types
    if py_type is str:
        return {"type": "string"}
    if py_type in (int, float):
        return {"type": "number"}
    if py_type is bool:
        return {"type": "boolean"}
    if py_type is type(None):
        return {"type": "null"}

    # List/array
    if origin in (list, typing.List):
        item_type = args[0] if args else str
        return {
            "type": "array",
            "items": python_type_to_json_type(item_type)
        }

    # Dict/object
    if origin in (dict, typing.Dict):
        value_type = args[1] if len(args) > 1 else str
        return {
            "type": "object",
            "additionalProperties": python_type_to_json_type(value_type)
        }

    # Union/Optional
    if origin is typing.Union:
        json_types = [python_type_to_json_type(a) for a in args]
        # Handle Optional[X] (Union[X, NoneType])
        non_null_types = [t for t in json_types if t.get("type") != "null"]
        if len(json_types) == 2 and len(non_null_types) == 1:
            result = non_null_types[0].copy()
            result["nullable"] = True
            return result
        return {"anyOf": json_types}

    # Fallback
    return {"type": "string"}

class ChatCompletionTool(JSONSerializable):
    """
    Base class for all chat completion tools.
    """
    def __init__(self, type_: str):
        """Initializes a ChatCompletionTool instance.

        :param type_: The type of the tool.
        :type type_: str
        """
        self.type = type_

    def to_dict(self) -> Dict[str, Any]:
        """Converts the ChatCompletionTool instance to a dictionary representation.

        :return: A dictionary representation of the ChatCompletionTool instance.
        :rtype: Dict[str, Any]
        """
        return {
            "type": self.type,
        }


class FunctionTool(ChatCompletionTool):
    """
    Represents a function tool for OpenAI-like function calling.
    """
    def __init__(
        self,
        name: str,
        parameters: dict,
        strict: bool = False,
        description: Optional[str] = None,
        function: Optional[Callable] = None,
    ):
        """Initializes a FunctionTool instance.

        :param name: The name of the function.
        :type name: str
        :param parameters: The parameters schema for the function.
        :type parameters: dict
        :param strict: Whether to enforce strict parameter checking, defaults to False
        :type strict: bool, optional
        :param description: The description of the function, defaults to None
        :type description: Optional[str], optional
        :param function: The actual callable function, defaults to None
        :type function: Optional[Callable], optional
        """
        super().__init__(type_="function")
        self.name = name
        self.description = description
        self.parameters = parameters
        self.strict = strict
        self.function = function

    def to_dict(self) -> Dict[str, Any]:
        """Converts the FunctionTool instance to a dictionary representation.

        :return: A dictionary representation of the FunctionTool instance.
        :rtype: Dict[str, Any]
        """
        base = {
            "type": self.type,
            "function": {
                "name": self.name,
                "parameters": self.parameters,
                "strict": self.strict,
            },
        }

        if self.description:
            base["function"]["description"] = self.description

        return base

    def execute(self, **kwargs: Any) -> Any:
        """Execute the function with the provided arguments.

        :raises ValueError: If the function is not set or if unexpected arguments are provided in strict mode.
        :return: The result of the function execution.
        :rtype: Any
        """
        if self.function is None:
            raise ValueError("Function is not set.")

        if self.strict:
            for key in kwargs.keys():
                if key not in self.parameters["properties"]:
                    raise ValueError(f"Unexpected argument '{key}' for function '{self.name}'")

        return self.function(**kwargs)

    async def aexecute(self, **kwargs: Any) -> Any:
        """Asynchronously execute the function with the provided arguments.

        :raises ValueError: If the function is not set or if unexpected arguments are provided in strict mode.
        :return: The result of the function execution.
        :rtype: Any
        """
        if self.function is None:
            raise ValueError("Function is not set.")

        if self.strict:
            for key in kwargs.keys():
                if key not in self.parameters["properties"]:
                    raise ValueError(f"Unexpected argument '{key}' for function '{self.name}'")

        return await self.function(**kwargs)


    @staticmethod
    def from_function(
            func: Callable,
            *,
            description: Optional[str] = None,
            strict: bool = False
    ) -> "FunctionTool":
        """Create a FunctionTool from a Python function.

        :param func: The Python function to convert.
        :type func: Callable
        :param description: The description of the function, defaults to None
        :type description: Optional[str], optional
        :param strict: Whether to enforce strict parameter checking, defaults to False
        :type strict: bool, optional
        :raises TypeError: If any parameter is missing a type hint.
        :return: A FunctionTool instance.
        :rtype: FunctionTool
        """

        tool_description = description or inspect.getdoc(func)
        sig = inspect.signature(func)
        type_hints = typing.get_type_hints(func)
        param_schema = {}

        for name, param in sig.parameters.items():
            if name not in type_hints:
                raise TypeError(
                    f"Parameter '{name}' in '{func.__name__}' is missing a type hint."
                )
            param_type = type_hints.get(name, str)
            param_schema[name] = python_type_to_json_type(param_type)

        parameters = {
            "type": "object",
            "properties": param_schema,
            "required": [
                name for name, param in sig.parameters.items()
                if param.default is inspect.Parameter.empty
            ],
            "additionalProperties": False
        }

        return FunctionTool(
            name=func.__name__,
            description=tool_description,
            parameters=parameters,
            strict=strict,
            function=func,
        )


def function_tool(
        func: Optional[Callable] = None, *, description: Optional[str] = None, strict: bool = False
) -> Callable[[Callable], FunctionTool] | FunctionTool:
    """Create a decorator that converts a function into a FunctionTool.
    
    Usage:
        
    @function_tool

    def my_func(...): ...

    @function_tool()

    def my_func(...): ...

    :param func: The function to convert, defaults to None
    :type func: Optional[Callable], optional
    :param description: The description of the function, defaults to None
    :type description: Optional[str], optional
    :param strict: Whether to enforce strict parameter checking, defaults to False
    :type strict: bool, optional
    :return: A FunctionTool instance or a decorator function.
    :rtype: Callable[[Callable], FunctionTool] | FunctionTool
    """

    def decorator(func_: Callable) -> FunctionTool:
        """Create a FunctionTool from the decorated function.

        :param func_: The decorated function.
        :type func_: Callable
        :return: A FunctionTool instance.
        :rtype: FunctionTool
        """
        return FunctionTool.from_function(func=func_, description=description, strict=strict)

    if func is not None and callable(func):
        # Used as @function_tool
        return decorator(func)
    else:
        # Used as @function_tool()
        return decorator
