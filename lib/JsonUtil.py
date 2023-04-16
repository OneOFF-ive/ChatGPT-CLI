import os
import json
from config import *


class JsonUtil:
    @staticmethod
    def json2Config(file_dir: str, file_name: str):
        # 获取当前文件所在目录的上级目录，也就是项目根目录
        root_path = os.path.dirname(os.path.abspath(__file__))
        root_path = os.path.abspath(os.path.join(root_path, '..'))

        # 构造json文件路径
        conf_path = os.path.join(root_path, file_dir, file_name)

        # 读取json文件内容
        with open(conf_path, 'r') as f:
            conf_data = json.load(f)

        # 将json数据序列化
        chatCompletionConfig = ChatCompletionConfig(**conf_data.get("CompletionConfig"))
        imageConfig = ImageConfig(**conf_data.get("ImageConfig"))
        transcriptionsConfig = TranscriptionsConfig(**conf_data.get("TranscriptionsConfig"))

        return chatCompletionConfig, imageConfig, transcriptionsConfig


__all__ = [
    "JsonUtil"
]
