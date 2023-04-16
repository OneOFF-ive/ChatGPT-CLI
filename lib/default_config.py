from JsonUtil import *

chatCompletionConfig, imageConfig, transcriptionsConfig = JsonUtil.json2Config("conf", "config.json")

__all__ = [
    "chatCompletionConfig",
    "imageConfig",
    "transcriptionsConfig"
]
