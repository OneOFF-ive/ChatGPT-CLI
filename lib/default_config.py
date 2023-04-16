from JsonUtil import *

completionConfig, imageConfig, transcriptionsConfig = JsonUtil.json2Config("conf", "config.json")

__all__ = [
    "completionConfig",
    "imageConfig",
    "transcriptionsConfig"
]
