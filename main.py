import os
import openai


def generateCompletion(msg):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=msg,
        temperature=1,
        n=1,
        stream=False,
        stop='\n',
        max_tokens=2048,
        presence_penalty=0,
        frequency_penalty=0,
    )


def getResult(completions):
    return completions.choices[0]["message"]["content"]


def main():
    openai.organization = "org-nQ2su19ado3KvvI9HE5vAZHO"
    openai.api_key = os.getenv("OPENAI_API_KEY")
    messages: list[dict] = [{"role": "system", "content": "You are a helpful assistant."}]
    while True:
        prompt: str = input()
        message: dict[str: str] = {"role": "user", "content": prompt}
        messages.append(message)

        result = getResult(generateCompletion(messages))
        messages.append({"role": "assistant", "content": result})
        print(result)


if __name__ == "__main__":
    main()
