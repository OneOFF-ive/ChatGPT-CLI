import os
import openai

openai.organization = "org-nQ2su19ado3KvvI9HE5vAZHO"
openai.api_key = os.getenv("OPENAI_API_KEY")
completions = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello!"}],
    temperature=1,
    n=1,
    stream=False,
    stop='\n',
    max_tokens=2048,
    presence_penalty=0,
    frequency_penalty=0,
)
message = completions.choices[0]["message"]["content"]
print(message)

