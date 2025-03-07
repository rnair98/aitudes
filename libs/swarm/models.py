import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator
from pydantic.dataclasses import dataclass
from typing import (
    Dict, 
    Iterable, 
    List, 
    Literal, 
    Optional, 
    Union
)   
from functools import partial

from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionModality,
    ChatCompletionAudioParam,
    ChatCompletionReasoningEffort,
    ChatCompletionPredictionContentParam,
    ChatCompletionStreamOptionsParam,
    ChatCompletionToolChoiceOptionParam,
    ChatCompletionToolParam,
    completion_create_params,
)
from openai.types.chat_model import ChatModel
from openai.types.shared import Metadata

load_dotenv()  

QUANTIZATIONS = Literal[
    "int4", 
    "int8", 
    "fp6", 
    "fp8",
    "fp16", 
    "bf16", 
    "fp32", 
    "unknown"
]

OPENROUTER_TAGS = Literal[
    "free", 
    "online", 
    "nitro", 
    "floor", 
]

MODEL_TYPES = Literal[
    "chat",
    "fast",
    "embeddings",
    "reasoning",
    "grounding",
]

MODEL_INPUTS = Literal[
    "text",
    "image",
    "audio",
    "video",
]
MODEL_OUTPUTS = Literal[
    "text",
    "image",
    "audio",
    "video",
]

REASONING_EFFORT = Literal[
    "low",
    "medium",
    "high",
]

REASONING_MODELS = (
    "o1",
    "o3-mini",
)

@dataclass
class Provider:
    name: str = "openai"
    api_key: Optional[str] = None
    base_url: str = "https://api.openai.com/v1"
    sort: Literal["price", "throughput", "latency"] = "price"
    order: List[str] = None
    allow_fallbacks: bool = False
    require_parameters: bool = True
    data_collection: Literal["allow", "deny"] = "allow"
    ignore: List[str] = None
    quantizations: List[QUANTIZATIONS] = None

    def __post_init__(self):
        if self.api_key is None:
            self.api_key = os.getenv("OPENAI_API_KEY")

@dataclass
class Model:
    provider: Provider = Field(default_factory=lambda: Provider())
    types: List[MODEL_TYPES] = None
    inputs: List[MODEL_INPUTS] = None
    outputs: List[MODEL_OUTPUTS] = None
    tags: List[OPENROUTER_TAGS] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []

class BaseChatCompletions(BaseModel):
    messages: Iterable[ChatCompletionMessageParam]
    model: Union[str, ChatModel]
    audio: Optional[ChatCompletionAudioParam] = None
    frequency_penalty: Optional[float] = Field(ge=-2.0, le=2.0, default=0)
    function_call: completion_create_params.FunctionCall = None
    functions: Iterable[completion_create_params.Function] = None
    logit_bias: Optional[Dict[str, int]] = None
    logprobs: Optional[bool] = None
    max_completion_tokens: Optional[int] = None
    max_tokens: Optional[int] = None
    metadata: Optional[Metadata] = None
    modalities: Optional[List[ChatCompletionModality]] = None
    n: Optional[int] = 1
    parallel_tool_calls: bool = None
    prediction: Optional[ChatCompletionPredictionContentParam] = None
    presence_penalty: Optional[float] = Field(ge=-2.0, le=2.0, default=0)
    reasoning_effort: Optional[ChatCompletionReasoningEffort] = None
    response_format: completion_create_params.ResponseFormat = None
    seed: Optional[int] = None
    service_tier: Optional[Literal["auto", "default"]] = None
    stop: Union[Optional[str], List[str]] = None
    store: Optional[bool] = None
    stream: Optional[Literal[False]] = None
    stream_options: Optional[ChatCompletionStreamOptionsParam] = None
    temperature: Optional[float] = None
    tool_choice: ChatCompletionToolChoiceOptionParam = None
    tools: Iterable[ChatCompletionToolParam] = None
    top_logprobs: Optional[int] = None
    top_p: Optional[float] = None
    user: str = None

    @field_validator("reasoning_effort", mode="after")
    @classmethod
    def check_reasoning_effort(cls, v, values):
        if v and values["model"] not in REASONING_MODELS:
            raise ValueError(
                f"Model {values['model']} does not support reasoning_effort"
            )
        return v

class PPLXChatCompletions(BaseChatCompletions):
    search_domain_filter: Optional[List[str]] = None
    return_images: bool = None
    return_related_questions: bool = None
    search_recency_filter: Optional[Literal["day", "week", "month", "hour"]] = None
    top_k: Optional[int] = Field(ge=0, le=2048, default=0)


open_router = partial(
    Provider, 
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL")
)

OR_OAI = open_router(name="openai")
OR_PPLX = open_router(name="perplexity")
OR_GOOGLE = open_router(name="google")
OR_XAI = open_router(name="xai")
OR_MISTRAL = open_router(name="mistralai")


OPENROUTER_MODELS = {
    "gpt-4o": Model(
        provider=OR_OAI,
        types=["chat"],
        inputs=["text", "image"],
        outputs=["text"],
    ),
    "gpt-4o-mini": Model(
        provider=OR_OAI,
        types=["chat", "fast"],
        inputs=["text", "image"],
        outputs=["text"],
    ),
    "o1": Model(
        provider=OR_OAI,
        types=["reasoning"],
    ),
    "o3-mini": Model(
        provider=OR_OAI,
        types=["reasoning", "fast"],
    ),
    "sonar": Model(
        provider=OR_PPLX,
        types=["chat", "grounding"],
    ),
    "sonar-reasoning": Model(
        provider=OR_PPLX,
        types=["reasoning", "grounding"],
    ),
    "r1-1776": Model(
        provider=OR_PPLX,
        types=["reasoning"],
    ),
    "gemini-2.0-flash-001": Model(
        provider=OR_GOOGLE,
        types=["chat", "fast", "grounding"],
    ),
    "gemini-2.0-pro-exp-02-05": Model(
        provider=OR_GOOGLE,
        types=["chat"],
        tags=["free"]
    ),
    "gemini-2.0-flash-thinking-exp": Model(
        provider=OR_GOOGLE,
        types=["reasoning"],
        tags=["free"]
    ),
    "grok-2-1212": Model(
        provider=OR_XAI,
        types=["chat"],
        inputs=["text"],
        outputs=["text"],
    ),
    "grok-2-vision-1212": Model(
        provider=OR_XAI,
        types=["chat"],
        inputs=["text", "image"],
        outputs=["text"],
    ),
    "mistral-small-24b-instruct-2501": Model(
        provider=OR_MISTRAL,
        types=["chat", "fast"],
        inputs=["text"],
        outputs=["text"],
        tags=["free"]
    )
}