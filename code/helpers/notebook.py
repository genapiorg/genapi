from termcolor import colored
from IPython.display import display, Markdown

from io import StringIO
import sys
import textwrap

# Courtesy https://github.com/aws-samples/amazon-bedrock-workshop/blob/main/utils/__init__.py
def print_ww(*args, width: int = 100, **kwargs):
    """Like print(), but wraps output to `width` characters (default 100)"""
    buffer = StringIO()
    try:
        _stdout = sys.stdout
        sys.stdout = buffer
        print(*args, **kwargs)
        output = buffer.getvalue()
    finally:
        sys.stdout = _stdout
    for line in output.splitlines():
        print("\n".join(textwrap.wrap(line, width=width)))

# Courtesy https://github.com/openai/openai-cookbook/blob/main/examples/How_to_call_functions_with_chat_models.ipynb
def print_chat(messages, system=False, function=False, last=True, all=False):
    if all:
        last = False
        function = True
        system = True
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }
    if last:
        messages = messages[-1:]
    for message in messages:
        if message["role"] == "system" and system:
            print(colored(f"system: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "user":
            print(colored(f"user: {message['content']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and message.get("function_call"):
            print(colored(f"assistant: {message['function_call']}\n", role_to_color[message["role"]]))
        elif message["role"] == "assistant" and not message.get("function_call"):
            print(colored(f"assistant:\n", role_to_color[message["role"]]))
            display(Markdown(f"{message['content']}\n"))
        elif message["role"] == "function" and function:
            print(colored(f"function ({message['name']}): {message['content']}\n", role_to_color[message["role"]]))