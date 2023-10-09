---
tags:
  - Functions
---

# OpenAI Functions with Climate APIs

Most popular user experience based on Large Language Models is the chat experience popularized by ChatGPT. Bard and Bing use cases of LLM follow a specialization of this chat experience in the form of questions and answers (Q&A). When enterprise build apps using LLMs, they are likely to use a combination of chat and Q&A experiences. These apps are more useful when they are able to integrate existing apps and services activated based on the context of the chat or Q&A experience. Think of this as a conversation with your assistant about a certain topic. At some point you may suggest actions for the assistant to execute based on the context of the conversation. This is where the concept of functions come in. Functions are a way to specify actions that can be executed based on the context of the conversation.

OpenAI [Functions](https://openai.com/blog/function-calling-and-other-api-updates) were introduced in July 2023 as a way for developers to have GPT 4 and GPT 3.5 models identify when to process user inputs and extract JSON arguments matching function specs specified in the chat context.

!!! tip "API Tips"
    You can specify a functions in a similar format as a typical function documentation describing the function name, description, arguments, and return values. GenAPI project structure recommends writing the function spec next to the function definition so that it is easy to keep both in sync with any future changes.

## Helper APIs and functions library

GenAPI helpers include wrappers for OpenAI APIs to maintain conversation context within a multi-step chat and perform question and action in a single-step dialog. We also include helpers for simulating chat like experience within a notebook and evaluating function calling within a conversation. 

```python title="Importing GenAPI Helper APIs and Functions Repository"
from helpers import genapi, notebook
from functions import climate
```

GenAPI also provides a functions library with a number of functions that can be used to build Generative AI Apps. The functions library is organized into a number of categories like the one we are launching for climate APIs which include weather and air quality functions. You can add these functions to your project like so.

```python title="Adding Climate Functions Repository"
functions = climate.functions
function_names = {
    "weather": climate.weather,
    "air_quality": climate.air_quality
}
```

## Initializing conversation context

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

This returns the following LLM response. Note that the LLM response is asking for arguments to fill in the weather function. This is possible because of two reasons. First, we have specified the function spec for the weather function and which arguments are required (you will see the function spec later in this article). Second, we have specified the system prompt to guide the LLM on how to handle functions.

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

## Maintaining conversation context

Now what if the user changes their mind and wants to weather in different city or has a preference for a diffrent unit? This is where power of LLM understanding natural language and maintaining context comes together. We are also able to do this because the `genapi.chat` helper API maintains the conversation context within the messages list. You can go on to converse with the simulated chatbot within your notebook by adding the following user prompt.

```python title="User prompt with changes in arguments"
messages.append({"role": "user", "content": "in Metric units please."})
messages = genapi.chat(messages, function_names, functions)
notebook.print_chat(messages)
```

This returns the following LLM response after calling the weather function with the revised units.

```yaml title="LLM response with revised units"
assistant: The current weather in Sunnyvale, CA, USA is overcast clouds with a temperature of
14.84°C.
```

## Switching conversation context

Now what if you wanted to switch the conversation to ask about air quality. Note that we are not specifying the location although the air quality function requires this argument. LLM will pick this up from prior context.

```python title="User prompt with air quality"
messages.append({"role": "user", "content": "and how is the air quality here."})
messages = genapi.chat(messages, function_names, functions)
notebook.print_chat(messages)
```

This returns the following LLM response after calling the air quality function with the user provided arguments.

```yaml title="LLM response with air quality information"
assistant: The air quality in Sunnyvale, California, USA is 43 AQI (Air Quality Index).
```

## Evaluating function calling

We can now evaluate the entire conversation flow to inspect how the LLM filled the arguments and called the required functions. We can also compare the function calls with the resulting LLM natural language generation.

```python title="Evaluating function calling"
notebook.print_chat(messages, all=True)
```

This returns the following LLM response with color coded (noticable in Notebook environment) messages alternating between user and assistant. Note that all messages apart from user and system are LLM generated.

```yaml title="LLM response with entire conversation flow"
system: Don't make assumptions about what values to plug into functions.
    Ask for clarification if a user request is ambiguous.

user: What's the weather today?

assistant: In which city are you interested in knowing the weather? Please provide the city
name, state code, and country.

user: I live in Sunnyvale, CA.

function (weather): {"location": "Sunnyvale, CA, USA", "temperature": 58.64, "units":
"Fahrenheit", "forecast": "overcast clouds"}

assistant: The current weather in Sunnyvale, CA, USA is overcast clouds with a temperature of
58.64°F.

user: in Metric units please.

function (weather): {"location": "Sunnyvale, CA, USA", "temperature": 14.84, "units":
"Celsius", "forecast": "overcast clouds"}

assistant: The current weather in Sunnyvale, CA, USA is overcast clouds with a temperature of
14.84°C.

user: and how is the air quality here.

user: and how is the air quality here.

function (air_quality): {"location": "Sunnyvale, California, USA", "air_quality": "43 AQI"}

assistant: The air quality in Sunnyvale, California, USA is 43 AQI (Air Quality Index).
```

## Evaluating question and answering

What if you wanted to evaluate various functions and their responses in a single step. This way you can try different prompt variations to see how the LLM handles each scenario. GenAPI helper API has got you covered.

```python title="Evaluating question and answering"
act_messages = [{"role": "user", "content": "What's the air quality in New York City, NY?"}]
print(genapi.act(act_messages, function_names, functions))
```

This generates the following response from LLM.

```yaml title="LLM response with air quality information"
The air quality in New York City, NY is currently 10 AQI, which is considered good.
```

## Function specifications

Now it is time to dive into the function specification itself. We start with the specification for weather function and then share the function code. Note that the LLM only needs the function specification to be able to identify the function to call.

Let's study the specification. Few noticable things are (1) the specification resembles function documentation with name, description, arguments, and return values, (2) the specification is written in JSON format, (3) the specification is written in a way that is easy for the LLM to understand, (4) the specification descriptions are crisp, and (5) the descriptions include example values where relevant.

```json title="Weather function specification"
weather_spec = {
    "name": "weather",
    "description": "Get the current weather",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "The city, e.g. San Francisco",
            },
            "state": {
                "type": "string",
                "description": "The state code, e.g. CA",
            },
            "country": {
                "type": "string",
                "description": "The country, e.g. USA",
            },
            "units": {
                "type": "string", 
                "enum": ["metric", "imperial"],
                "description": "Units to use when reporting weather data.",
            },
        },
        "required": ["city", "state", "country"],
    },
}
```

Once LLM identifies the function, the developer can then call the function and return the result to the LLM. The LLM will then use the result to generate the natural language response.

Let's note some important points which help in integrating the function with an LLM. First, the function takes in arguments in the same sequence as in the specification. Second, the required arguments match the speficication and any arguments that are not required have a default value set. Third, when calling external APIs, the function is able to gracefully handle errors and return a JSON response with an error message. Fourth, the function returns a JSON response with keys identifiable in plain English by the LLM. Fifth, the return value JSON object keys are not defined in the specification. LLM is able to convert this JSON response into natural language response without the need for a specification.

```python title="Weather function code"
def weather(city, state, country, units="imperial"):
    api_key = os.getenv("OPEN_WEATHER_MAP_KEY")
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    complete_api_link = f"{base_url}?q={city},{state},{country}&units={units}&appid={api_key}"
    
    response = requests.get(complete_api_link)
    
    if response.status_code != 200:
        return json.dumps({"error": "Unable to fetch weather data"})
    
    data = response.json()
    
    weather_info = {
        "location": f"{city}, {state}, {country}",
        "temperature": data['main']['temp'],
        "units": 'Celsius' if units == 'metric' else 'Fahrenheit',
        "forecast": data['weather'][0]['description'],
    }
    return json.dumps(weather_info)
```

Let us now read the specification for the air quality function and then share the function code. Note that the specification is similar to the weather function specification. The only difference is that the air quality function does not have a units argument.

```json title="Air quality function specification"
air_quality_spec = {
    "name": "air_quality",
    "description": "Get the current air quality",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "The city, e.g. San Francisco",
            },
            "state": {
                "type": "string",
                "description": "The full form state name, e.g. California",
            },
            "country": {
                "type": "string",
                "description": "The country, e.g. USA",
            },
        },
        "required": ["city", "state", "country"],
    },
}
```

The air quality function code is similar to the weather function code. The only difference is that the air quality function does not have a units argument.

```python title="Air quality function code"
def air_quality(city, state, country):
    api_key = os.getenv("IQAIR_KEY")
    base_url = 'http://api.airvisual.com/v2/city'
    parameters = {'city': city, 'state': state, 'country': country, 'key': api_key}
    response = requests.get(base_url, params=parameters)
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'current' in data['data'] and 'pollution' in data['data']['current']:
            aqi = data['data']['current']['pollution']['aqius']
            air_quality_info = {
                "location": f"{city}, {state}, {country}",
                "air_quality": f"{aqi} AQI",
            }
            return json.dumps(air_quality_info)
        else:
            raise Exception("Data format is not as expected, or data not available for the requested city.")
    else:
        raise Exception(f"Failed to retrieve data: {response.status_code}")
```

Now all that is required is to add the function specifications to the function library so these can be easily imported in our notebook.

```python title="Adding function specifications to function library"
functions = []
functions.append(weather_spec)
functions.append(air_quality_spec)
```

This structure where related functions are grouped together in a functions library is a recommended best practice for building Generative AI Apps. This enables building modular LLM apps which only need to import functions based on the use case. Combining functions from multiple libraries is also as easy as importing multiple libraries and merging the imported arrays.

## Conclusion

You can access GenAPI cookbook here [OpenAI Functions with Climate APIs](https://github.com/genapiorg/genapi/blob/main/cookbook/openai-functions-with-climate-apis.ipynb). You can also reuse the helper API code for genapp and notebook from GitHub [code/helpers](https://github.com/genapiorg/genapi/tree/main/code/helpers) folder. The functions library is available in the GitHub [code/functions](https://github.com/genapiorg/genapi/tree/main/code/functions) folder where you can study the `climate.py` file for the functions used in this article.



