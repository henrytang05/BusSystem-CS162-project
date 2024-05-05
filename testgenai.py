import pathlib
import textwrap
import time

import google.generativeai as genai


from IPython import display
from IPython.display import Markdown


def to_markdown(text):
    text = text.replace("•", "  *")
    return Markdown(textwrap.indent(text, "> ", predicate=lambda _: True))


def multiply(a: float, b: float):
    """returns a * b."""
    return a * b


def NLP():

    try:
        # Used to securely store your API key

        # Or use `os.getenv('API_KEY')` to fetch an environment variable.

        import os

        GOOGLE_API_KEY = os.getenv("API_KEY")
    except ImportError:
        import os

        GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]

    genai.configure(api_key=GOOGLE_API_KEY)

    model = genai.GenerativeModel(model_name="gemini-1.0-pro", tools=[multiply])
    chat = model.start_chat(enable_automatic_function_calling=True)

    response = chat.send_message(
        "I have 57 cats, each owns 44 mittens, how many mittens is that in total?"
    )
    print(response.text)


NLP()
