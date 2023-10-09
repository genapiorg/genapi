---
tags:
  - Functions
---

# OpenAI Functions with Climate APIs

Most popular user experience based on Large Language Models is the chat experience popularized by ChatGPT. Bard and Bing use cases of LLM follow a specialization of this chat experience in the form of questions and answers (Q&A). When enterprise build apps using LLMs, they are likely to use a combination of chat and Q&A experiences. These apps are more useful when they are able to integrate existing apps and services activated based on the context of the chat or Q&A experience. Think of this as a conversation with your assistant about a certain topic. At some point you may suggest actions for the assistant to execute based on the context of the conversation. This is where the concept of functions come in. Functions are a way to specify actions that can be executed based on the context of the conversation.

OpenAI [Functions](https://openai.com/blog/function-calling-and-other-api-updates) were introduced in July 2023 as a way for developers to have GPT 4 and GPT 3.5 models identify when to process user inputs and extract JSON arguments matching function specs specified in the chat context.

!!! tip "API Tips"
    You can specify a functions in a similar format as a typical function documentation describing the function name, description, arguments, and return values. GenAPI project structure recommends writing the function spec next to the function definition so that it is easy to keep both in sync with any future changes.

## Helper APIs and Functions Repository

GenAPI helpers include wrappers for OpenAI APIs to maintain conversation context within a multi-step chat and perform question and action in a single-step dialog. We also include helpers for simulating chat like experience within a notebook and evaluating function calling within a conversation. 

```python title="Importing GenAPI Helper APIs and Functions Repository"
from helpers import genapi, notebook
from functions import climate
```

GenAPI also provides a functions repository with a number of functions that can be used to build Generative AI Apps. The functions repository is organized into a number of categories like the one we are launching for climate APIs which include weather and air quality functions. You can add these functions to your project like so.

```python title="Adding Climate Functions Repository"
functions = climate.functions
function_names = {
    "weather": climate.weather,
    "air_quality": climate.air_quality
}
```

## Initializing Conversation Context

You can now initialize the conversation context with a **system prompt** to guide the LLM how to handle functions. 

```python title="Initializing Conversation Context"
messages = []
messages.append(
  {
    "role": "system", 
    "content": '''Don't make assumptions about what values to plug into 
    functions. Ask for clarification if a user request is ambiguous.'''
  })
```

System prompts in the context of the GPT-3 API (and GPT-4 and other similar models) refer to the initial input given to the model to generate a particular kind of response. They set the context or tone for the generated text and guide the model's responses.

!!! tip "LLM Tips"
    To enable iterative argument filling by the LLM where the LLM asks for missing arguments, you can use the System Prompt to guide the LLM on how to handle functions.

For example, you could use a system prompt like "You are a helpful assistant that provides detailed and informative responses." This prompt sets the model in a context where it acts as a helpful assistant and aims to provide detailed answers to questions.

Another distinction of a system prompt is that it is app developer initiated instead of user initiated prompts or LLM initiated responses. By appending the system prompt to the messages list, the app developer is able to maintain control over the conversation context, hidden from the user who would usually see their own prompts and LLM responses only.

## Simulating chat experience

You can now simulate a chat experience within a notebook using the `genapi.chat` helper API. This helper API takes in the messages list and the function repository and returns a list of messages with the LLM responses. Then the helper API `notebook.print_chat` can be used to print the chat experience within the notebook one cell at a time.

```python title="Initial user prompt"
messages.append({"role": "user", "content": "What's the weather today?"})
messages = genapi.chat(messages, function_names, functions)
notebook.print_chat(messages)
```

This returns the following LLM response.

```yaml title="LLM response asking for argument filling"
assistant: In which city are you interested in knowing the weather? 
Please provide the city name, state code, and country.
```

You can go on to converse with the simulated chatbot within your notebook by adding the following user prompt.

```python title="User prompt with arguments"
messages.append({"role": "user", "content": "I live in Sunnyvale, CA."})
messages = genapi.chat(messages, function_names, functions)
notebook.print_chat(messages)
```

This returns the following LLM response after calling the weather function with the user provided arguments.

```yaml title="LLM response with weather information"
assistant: The current weather in Sunnyvale, CA, USA is overcast clouds 
with a temperature of 58.64°F.
```





