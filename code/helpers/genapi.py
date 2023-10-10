import json
import openai
import requests
from tenacity import retry, wait_random_exponential, stop_after_attempt

GPT_MODEL = "gpt-3.5-turbo-0613"

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, functions=None, function_call=None, model=GPT_MODEL):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }
    json_data = {"model": model, "messages": messages}
    if functions is not None:
        json_data.update({"functions": functions})
    if function_call is not None:
        json_data.update({"function_call": function_call})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

def chat(messages, function_names, functions):
    chat_response = chat_completion_request(
        messages, functions=functions
    )
    assistant_message = chat_response.json()["choices"][0]["message"]
    if "function_call" in assistant_message:
        function_name = assistant_message["function_call"]["name"]
        function_call = function_names[function_name]
        function_args = assistant_message['function_call']['arguments']
        
        # generic function call, assumes arguments in same sequence as function spec
        function_response = function_call(*list(json.loads(function_args).values()))
        messages.append({"role": "function", "name": function_name, "content": function_response,})
        chat_response = chat_completion_request(
            messages, functions=functions
        )
        assistant_message = chat_response.json()["choices"][0]["message"]
    
    # recursively handle multiple function calls within same user prompt
    if "function_call" in assistant_message:
        messages = chat(messages, function_names, functions)
    else:
        messages.append(assistant_message)
    return messages

def act(messages, function_names, functions):
    response = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=messages,
        functions=functions,
        function_call="auto",
    )
    response_message = response["choices"][0]["message"]

    if response_message.get("function_call"):
        function_name = response_message["function_call"]["name"]
        function_to_call = function_names[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = function_to_call(*list(function_args.values())
        )

        messages.append(response_message)
        messages.append({"role": "function", "name": function_name, "content": function_response,}
        )
        second_response = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=messages,
        )
        return second_response["choices"][0]["message"]["content"]
    else:
        return response_message["content"]