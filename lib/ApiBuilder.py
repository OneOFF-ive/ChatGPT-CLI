import os
import openai

from Log import Log
import default_config

openai.api_key = os.getenv("OPENAI_API_KEY")
Log.info("inited")


class ApiBuilder:

    @staticmethod
    def ChatCompletion(msg: list[dict]):
        return openai.ChatCompletion.create(
            messages=msg,
            **default_config.chatCompletionConfig
        )

    @staticmethod
    def Image(prompt: str):
        Log.info("Picture Generating")
        res = openai.Image.create(
            prompt=prompt,
            **default_config.imageConfig
        )
        Log.info("Picture Generated")
        return res

    @staticmethod
    def Transcriptions(fileName: str):
        try:
            with open(fileName, "rb") as file:
                Log.info("Audio Translating")
                res = openai.Audio.translate(
                    file=file,
                    **default_config.transcriptionsConfig
                )
                Log.info("Audio Translated")
                return res
        except FileNotFoundError:
            Log.error("File Not Found")
