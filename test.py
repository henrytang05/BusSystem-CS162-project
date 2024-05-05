import pandas as pd
import os
import ast
from shapely.geometry import LineString, mapping
import google.ai.generativelanguage as glm
from geojson import Feature, FeatureCollection, Point
import json
from src.models.RouteVar import RouteVarHandler
from src.models.Path import PathHandler
from src.models.Graph import Graph
from src.models.Stop import StopHandler


def stop():

    w = StopHandler().load()
    r = RouteVarHandler()
    p = PathHandler().load()
    rse = r.get_var(85, 2)
    co = rse.convert_to_geojson()
    with open("output/route.geojson", "w") as file:
        file.write(str(FeatureCollection(co)))


def export_geojson(start=2028, end=7208):
    graph = Graph()
    co, co_var = graph.Dijkstra(start, end).convert_to_geojson()
    with open("output/route.geojson", "w") as file:
        file.write(str(FeatureCollection(co)))
    with open("output/route_var.geojson", "w") as file:
        file.write(str(FeatureCollection(co_var)))


def NLP():

    import pathlib
    import textwrap
    import time
    import os
    import google.generativeai as genai

    from IPython import display
    from IPython.display import Markdown

    try:
        GOOGLE_API_KEY = os.getenv("API_KEY")
    except ImportError:
        import os

        GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]

    genai.configure(api_key=GOOGLE_API_KEY)

    calculator = {
        "function_declarations": [
            {
                "name": "multiply",
                "description": "Returns the product of two numbers.",
                "parameters": {
                    "type_": "OBJECT",
                    "properties": {"a": {"type_": "NUMBER"}, "b": {"type_": "NUMBER"}},
                    "required": ["a", "b"],
                },
            }
        ]
    }
    model = genai.GenerativeModel("gemini-pro", tools=calculator)
    chat = model.start_chat()

    response = chat.send_message(
        f"What's 234551 X 325552 ?",
    )
    # fc = response.candidates[0].content.parts[0].function_call
    # print(fc)
    print(response.text)


def multiply(a: float, b: float):
    """returns a * b."""
    return a * b


def main():
    NLP()


main()
