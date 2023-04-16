from dataclasses import dataclass


@dataclass
class ChatCompletionConfig:
    system_prompt: str
    model: str
    temperature: int
    n: int
    stream: bool
    stop: str
    max_tokens: int
    presence_penalty: int
    frequency_penalty: int


@dataclass
class ImageConfig:
    n: int
    size: str
    response_format: str


@dataclass
class TranscriptionsConfig:
    model: str
    response_format: str


__all__ = [
    "ChatCompletionConfig",
    "ImageConfig",
    "TranscriptionsConfig"
]
