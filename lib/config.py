from dataclasses import dataclass


@dataclass
class ChatCompletionConfig:
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


@dataclass
class Config:
    chatCompletionConfig: ChatCompletionConfig
    imageConfig: ImageConfig
    transcriptionsConfig: TranscriptionsConfig
    conversations: int
    auto_modify_cons: bool


__all__ = [
    "ChatCompletionConfig",
    "ImageConfig",
    "TranscriptionsConfig",
    "Config"
]
