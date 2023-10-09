---
tags:
  - Functions
---

# OpenAI Functions with Climate APIs

Most popular user experience based on Large Language Models is the chat experience popularized by ChatGPT. Bard and Bing use cases of LLM follow a specialization of this chat experience in the form of questions and answers (Q&A). When enterprise build apps using LLMs, they are likely to use a combination of chat and Q&A experiences. These apps are more useful when they are able to integrate existing apps and services activated based on the context of the chat or Q&A experience. Think of this as a conversation with your assistant about a certain topic. At some point you may suggest actions for the assistant to execute based on the context of the conversation. This is where the concept of functions come in. Functions are a way to specify actions that can be executed based on the context of the conversation.

OpenAI [Functions](https://openai.com/blog/function-calling-and-other-api-updates) were introduced in July 2023 as a way for developers to have GPT 4 and GPT 3.5 models identify when to process user inputs and extract JSON arguments matching function specs specified in the chat context.

!!! tip info "API Tips"
    You can specify a functions in a similar format as a typical function documentation describing the function name, description, arguments, and return values. GenAPI project structure recommends writing the function spec next to the function definition so that it is easy to keep both in sync with any future changes.

## Helper APIs and Functions Repository
GenAPI helpers include wrappers for OpenAI APIs to maintain conversation context within a multi-step chat and perform question and action in a single-step dialog. We also include helpers for simulating chat like experiemce within a notebook and evaluating function calling within a conversation. 

```python title="Importing GenAPI Helper APIs and Functions Repository"
from helpers import genapi, notebook
from apis import climate
```

GenAPI also provides a functions repository with a number of functions that can be used to build Generative AI Apps. The functions repository is organized into a number of categories like the one we are launching with for climate APIs which include weather and air quality functions. We can add these functions to our project like so.

```python title="Adding Climate Functions Repository"
functions = climate.functions
function_names = {
    "weather": climate.weather,
    "air_quality": climate.air_quality
}
```



