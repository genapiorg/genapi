---
title: OpenAI Functions
tags:
  - Functions
  - OpenAI
  - Guidance
---

# OpenAI Functions

Most popular user experience based on Large Language Models is the chat experience popularized by ChatGPT. Bard and Bing use cases of LLM follow a specialization of this chat experience in the form of questions and answers (Q&A). When enterprise build apps using LLMs, they are likely to use a combination of chat and Q&A experiences. These apps are more useful when they are able to integrate existing apps and services activated based on the context of the chat or Q&A experience. Think of this as a conversation with your assistant about a certain topic. At some point you may suggest actions for the assistant to execute based on the context of the conversation. This is where the concept of functions come in. Functions are a way to specify actions that can be executed based on the context of the conversation.

OpenAI [Functions](https://openai.com/blog/function-calling-and-other-api-updates) were introduced in July 2023 as a way for developers to have GPT 4 and GPT 3.5 models identify when to process user inputs and extract JSON arguments matching function specs specified in the chat context.

## Guidance for using OpenAI Functions

This section is a collection of tips based on our experience using OpenAI Functions.

### Simple project structure 

GenAPI project structure recommends writing the function spec next to the function definition so that it is easy to keep both in sync with any future changes.

### System message

Use system prompt or meta prompt to instruct GPT model to (a) ask user for arguments instead of hallicunating or making assumptions, (b) call function only once per conversation step, (c) control how the LLM treats function response, and (d) control how the LLM responds.

```python title="System prompt to instruct GPT model"
messages.append(
    {
        "role": "system", 
        "content": '''Ask the user for arguments when calling a function. 
        Respond after understanding function response and user intent, if they expect,
        function response only or
        function response and your response.
        Don't call the same function more than once for each user prompt.
        Remain crisp and to the point in your responses.'''
    })
```

### Simple specifications 

You can specify a function spec in a similar format as a typical function documentation describing the function name, description, arguments, and return values. Start with minimal description, provide an example where applicable, test the function, and add more details as needed.


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

### Function definition guidance

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

## Techniques for using functions with LLMs

### LLM response based on function response

Most common use of functions is where you want the LLM response to be based on the function response. For example, you may want to ask the user for a city and state and then call the weather function to get the weather for the specified location. You may then want to respond to the user with the weather information. In this case, you can use the function response as the LLM response. See example in the cookbook [OpenAI Functions with Climate APIs](openai-functions-with-climate-apis.md) for more details.


### Combining multiple function calls in a single response

You may want to combine multiple function calls in a single response. For example, you may want to ask the user for a city and state and then call the weather and air quality function. You may then want to respond to the user with the weather and air quality information. In this case, you can use multiple function responses as the LLM response. GenAPI enables combining two or more functions in same response. See example in the cookbook [OpenAI Functions with Climate APIs](openai-functions-with-climate-apis.md) for more details.

### Function response overriding LLM response

You may want to override the LLM response with the function response. For example, user may want to render a painting with specific arguments. The LLM may also be able to generate an image however you may prefer to use the function response to create a custom painting based on user arguments. In this case, you can use the function response to override the LLM response. See example in the cookbook [OpenAI Functions with Render APIs](openai-functions-with-render-apis.md) for more details.

### Combining function response and LLM response

Sometimes you want LLM to generate certain response, like a Markdown table of top 5 tallest buildings in the world. Then you may want to call a function to genrate a chart based on this table. Then you are interested in combining function response and LLM response when responding to the user. See example in the cookbook [OpenAI Functions with Render APIs](openai-functions-with-render-apis.md) for more details.

## Reusable functions library

### Weather

Weather function is a simple function that takes in city, state, and country as arguments and returns the current weather for the specified location. The function uses OpenWeatherMap API to fetch the weather data. The function returns a JSON response with the following keys: location, temperature, units, and forecast. The function is available in the [functions library](https://github.com/genapiorg/genapi/blob/main/code/functions/climate.py) on the GenAPI GitHub.

### Air Quality

Air quality function is a simple function that takes in city, state, and country as arguments and returns the current air quality for the specified location. The function uses IQAir Air Visual API to fetch the air quality data. The function returns a JSON response with the following keys: location and air quality index. The function is available in the [functions library](https://github.com/genapiorg/genapi/blob/main/code/functions/climate.py) on the GenAPI GitHub.

### Molecule Inventor

We introduce a new GenAPI render function for visualizing molecules using SMILES string. Simplified molecular-input line-entry system or SMILES is a specification in the form of a line notation for describing the structure of chemical species using short ASCII strings. SMILES strings can be imported by most molecule editors for conversion back into two-dimensional drawings or three-dimensional models of the molecules.

This function requires GPT-4 to work as GPT-3.5 does not generate SMILES strings. Let us start by writing the function specification and definition. The function is available in the [functions library](https://github.com/genapiorg/genapi/blob/main/code/functions/render.py) on the GenAPI GitHub.


### Painting generator

Painting function is used to generate a painting based on given user inputs on painting subject, background, etc. We tried to design our API will a lot of flexibility in terms of the input parameters. At the same time our required arguments are minimal to keep prompt variations from simple to more involved. The function is available in the [functions library](https://github.com/genapiorg/genapi/blob/main/code/functions/render.py) on the GenAPI GitHub.


### Chart generator

Chart function is used to generate a chart based on the LLM response as a Markdown table. We can choose to render a bar, line, or point chart. The function is available in the [functions library](https://github.com/genapiorg/genapi/blob/main/code/functions/render.py) on the GenAPI GitHub.



