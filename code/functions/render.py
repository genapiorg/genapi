import json
import openai
from IPython.display import display, Image
import pandas as pd
from io import StringIO
import seaborn as sns
import matplotlib.pyplot as plt

painting_spec = {
    "name": "painting",
    "description": "Generate a painting.",
    "parameters": {
        "type": "object",
        "properties": {
            "subject": {
                "type": "string",
                "description": "Subject of the painting, e.g. astronaut.",
            },
            "setting": {
                "type": "string",
                "description": "Background or backdrop for the painting, e.g. alien landscape.",
            },
            "medium": {
                "type": "string",
                "description": "Medium used for the painting, e.g. oil.",
            },
            "surface": {
                "type": "string",
                "description": "Surface used for the painting, e.g. canvas.",
            },
            "artist": {
                "type": "string",
                "description": "A well known artist, e.g. Picasso.",
            },
            "size": {
                "type": "string",
                "description": "Size of image to generate in pixels heightxwidth format, e.g. 1024x512",
            },
        },
        "required": ["subject", "background"],
    },
}

def painting(subject, background, medium="oil", surface="canvas", artist="picasso", size='512x512'):
    prompt = f"Painting of {subject} in a {background} setting, painted in {medium} on {surface} by {artist}."
    response = openai.Image.create(
            prompt=prompt,
            n=1,
            size=size
        )
    image_url = response['data'][0]['url']
    display(Image(url=image_url))

    painting_info = {
        "prompt": prompt,
        "success": "Share this image link",
        "image_url": image_url,
    }
    return json.dumps(painting_info)


table_chart_spec = {
    "name": "table_chart",
    "description": "Render a chart based on a give Markdown table.",
    "parameters": {
        "type": "object",
        "properties": {
            "markdown_table": {
                "type": "string",
                "description": "Markdown table of data to render as a chart.",
            },
            "chart_type": {
                "type": "string", 
                "enum": ["point", "bar", "line"],
                "description": "Type of chart to render.",
            },
        },
        "required": ["markdown_table", "chart_type"],
    },
}

def is_alphanumeric(s):
    return s.isalnum() and (not s.isnumeric())

def table_chart(markdown_table, chart_type="bar"):
    df = pd.read_table(StringIO(markdown_table), sep="|").dropna(axis=1, how="all")
    df.columns = df.columns.str.strip()
    df = df.applymap(str.strip)
    df = df.iloc[1:].reset_index(drop=True)

    for col in df.columns:
        if df[col].apply(is_alphanumeric).all():
            continue
        
        try:
            df[col] = pd.to_numeric(df[col])
        except ValueError:
            pass

    if 'Rank' in df.columns:
        df = df.drop(columns=['Rank'])

    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except ValueError:
            pass

    string_columns = df.select_dtypes(include=['object']).columns.tolist()
    numeric_columns = df.select_dtypes(exclude=['object']).columns.tolist()

    if not string_columns or not numeric_columns:
        raise ValueError("Table must contain at least one string and one numeric column")

    string_column = string_columns[0]
    numeric_column = numeric_columns[0]

    if chart_type == 'bar':
        sns.barplot(x=numeric_column, y=string_column, hue=string_column, data=df, dodge=False, legend=False)
        plt.legend([],[], frameon=False)
    elif chart_type == 'line':
        sns.lineplot(x=numeric_column, y=string_column, hue=string_column, data=df, legend=False)
        plt.legend([],[], frameon=False)
    elif chart_type == 'point':
        sns.scatterplot(x=numeric_column, y=string_column, hue=string_column, data=df, legend=False)
        plt.legend([],[], frameon=False)
    else:
        raise ValueError("Unsupported chart type")

    plt.show()
    
    table_chart_info = {
        "success": "Rendered table as a chart.",
        "table": markdown_table,
    }
    return json.dumps(table_chart_info)


functions = []
functions.append(painting_spec)
functions.append(table_chart_spec)
