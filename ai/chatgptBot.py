from openai import OpenAI
import os
from dotenv import load_dotenv, dotenv_values
load_dotenv()


api_key = os.getenv("OPENAI_KEY")
client = OpenAI(
    api_key=api_key,
)

def messageChatgpt(message):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a crypto finance helper, keep responses short and simple"
            },
            {
                "role": "user",
                "content": message,
            },
        ],
    )
    return completion.choices[0].message.content
print(messageChatgpt("Hello"))