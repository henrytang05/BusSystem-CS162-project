from src.models.Graph import Graph
from src.models.StopQuery import StopQuery
from src.models.RouteVarQuery import RouteVarQuery
from src.models.Stop import *
from src.models.RouteVar import *

import google.generativeai as genai
import google.ai.generativelanguage as glm


def output_all_pairs_Dijkstra():

    g = Graph()
    g.Dijkstra_all_pairs_and_record_csv()


def get_top_k_stop():
    g = Graph()
    import time

    st = time.perf_counter()
    for res in g.Dijkstra_all_pairs():
        pass
    et = time.perf_counter()
    print(f"Dijkstra all pairs time: {et-st}")
    g.get_top_k_important_stops()


def NLP():
    try:
        import os

        GOOGLE_API_KEY = os.getenv("API_KEY")
    except ImportError:
        import os

        GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
    RouteVarHandler().load()
    StopHandler().load()
    genai.configure(api_key=GOOGLE_API_KEY)
    searcher = {
        "function_declarations": [
            {
                "name": "StopQuerysearch",
                "description": "Input query of (field, value) returns a list of stops with the following criteria:\n"
                "- StopId: int (Unique identifier for the stop)\n"
                "- Code: str (Code associated with the stop)\n"
                "- Name: str (Name of the stop)\n"
                "- StopType: str (Type of the stop)\n"
                "- Zone: str (Zone where the stop is located)\n"
                "- Ward: str (Ward where the stop is located)\n"
                "- AddressNo: str (Address number of the stop)\n"
                "- Street: str (Street where the stop is located)\n"
                "- SupportDisability: str (Indicates if the stop supports disability)\n"
                "- Status: str (Status of the stop)\n"
                "- Lng: float (Longitude coordinate of the stop)\n"
                "- Lat: float (Latitude coordinate of the stop)\n"
                "- Search: str (Field for general search)\n"
                "- Routes: str (Routes associated with the stop)\n",
                "parameters": {
                    "type_": "OBJECT",
                    "properties": {
                        "field": {"type_": "STRING"},
                        "value": {"type_": "STRING"},
                    },
                    "required": ["field", "value"],
                },
            }
        ]
    }
    searcher = glm.Tool(searcher)
    model = genai.GenerativeModel(
        model_name="gemini-pro",
        tools=[searcher],
    )
    print(model)
    chat = model.start_chat()

    print("here")
    response = chat.send_message("find stop with the code bx38")
    print("done")
    print(response)
    fc = response.candidates[0].content.parts[0].function_call
    f = fc.args["field"]
    v = fc.args["value"]
    r = StopQuery().search(f, v)
    print(r)


def main():
    NLP()


if __name__ == "__main__":
    main()
