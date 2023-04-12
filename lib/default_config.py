from lib.JsonUtil import JsonUtil
from lib.config import Config, ChatCompletionConfig, ImageConfig, TranscriptionsConfig

data = JsonUtil.json2Map("conf", "config.json")
default_config = Config(
    chatCompletionConfig=ChatCompletionConfig(**data.get("ChatCompletionConfig")),
    imageConfig=ImageConfig(**data.get("ImageConfig")),
    transcriptionsConfig=TranscriptionsConfig(**data.get("TranscriptionsConfig")),
    conversations=data.get("conversations"),
    auto_modify_cons=data.get("auto_modify_cons")
)

__all__ = [
    "default_config"
]
