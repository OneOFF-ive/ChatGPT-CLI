from JsonUtil import *
from config import *

data = JsonUtil.json2Map("conf", "config.json")
default_config = Config(
    chatCompletionConfig=ChatCompletionConfig(**data.get("ChatCompletionConfig")),
    imageConfig=ImageConfig(**data.get("ImageConfig")),
    transcriptionsConfig=TranscriptionsConfig(**data.get("TranscriptionsConfig")),
    **data
)

__all__ = [
    "default_config"
]
