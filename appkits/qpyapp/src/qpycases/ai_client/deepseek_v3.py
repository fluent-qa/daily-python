import json
import os
from typing import Dict

from dotenv import load_dotenv
from openai import OpenAI, BaseModel

load_dotenv()

deepseek_api_key = os.getenv("DEEP_SEEK_API_KEY")
client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")
beta_seek_url = "https://api.deepseek.com/beta"


# Coding / Math   	0.0
# Data Cleaning / Data Analysis	1.0
# General Conversation	1.3
# Translation	1.3
# Creative Writing / Poetry	1.5

def get_all_models():
    result = client.models.list()
    print(result)


class BalanceInfo(BaseModel):
    currency: str
    total_balance: str
    granted_balance: str
    topped_up_balance: str


def get_user_balance():
    result = client.get("user/balance", cast_to=BalanceInfo)
    print(result)


def code_completion():
    response = client.completions.create(
        model="deepseek-chat",
        prompt="def fib(a):",
        suffix="    return fib(a-1) + fib(a-2)",
        max_tokens=128
    )
    print(response)


def multiple_rounds_use_case():
    # Round 1
    messages = [{"role": "user", "content": "What's the highest mountain in the world?"},
                # {"role": "assistant", "content": "```python\n", "prefix": True} beta
                ]
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )

    messages.append(response.choices[0].message)
    print(f"Messages Round 1: {messages}")

    # Round 2
    messages.append({"role": "user", "content": "What is the second?"})
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )

    messages.append(response.choices[0].message)
    print(f"Messages Round 2: {messages}")


def json_output_use_case():
    system_prompt = """
    The user will provide some exam text. Please parse the "question" and "answer" and output them in JSON format. 

    EXAMPLE INPUT: 
    Which is the highest mountain in the world? Mount Everest.

    EXAMPLE JSON OUTPUT:
    {
        "question": "Which is the highest mountain in the world?",
        "answer": "Mount Everest"
    }
    """

    user_prompt = "Which is the longest river in the world? The Nile River."

    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}]

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        response_format={
            'type': 'json_object'
        }
    )

    print(json.loads(response.choices[0].message.content))


def send_messages(messages, tools):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools
    )
    return response.choices[0].message


def function_call_use_case():
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get weather of an location, the user should supply a location first",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        }
                    },
                    "required": ["location"]
                },
            }
        },
    ]

    messages = [{"role": "user", "content": "How's the weather in Hangzhou?"}]
    message = send_messages(messages, tools)
    print(f"User>\t {messages[0]['content']}")

    tool = message.tool_calls[0]
    messages.append(message)

    messages.append({"role": "tool", "tool_call_id": tool.id, "content": "24℃"})
    message = send_messages(messages, tools)
    print(f"Model>\t {message.content}")


if __name__ == '__main__':
    get_all_models()
    get_user_balance()
    # multiple_rounds_use_case()
