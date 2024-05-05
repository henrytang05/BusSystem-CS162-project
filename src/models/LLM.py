import google.generativeai as genai
import google.ai.generativelanguage as glm

from src.models.RouteVar import RouteVarHandler
from src.models.Stop import StopHandler
from src.models.Path import PathHandler
from src.models.StopQuery import StopQuery
from src.models.RouteVarQuery import RouteVarQuery
from src.models.PathQuery import PathQuery
import os


def query_with_llm(qr: str):
    RouteVarHandler().load()
    StopHandler().load()
    PathHandler().load()
    r = RouteVarQuery()
    s = StopQuery()
    p = PathQuery()
    try:
        GOOGLE_API_KEY = os.getenv("API_KEY")
        genai.configure(api_key=GOOGLE_API_KEY)
    except ImportError:
        import os

        GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
        genai.configure(api_key=GOOGLE_API_KEY)

    funcs = {
        "function_declarations": [
            {
                "name": "stopsearch",
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
            },
            {
                "name": "varsearch",
                "description": "Input query of (field, value) returns a list of route variables with the following criteria:\n"
                "- RouteId: int (Unique identifier for the route)\n"
                "- RouteVarId: int (Unique identifier for the route variable)\n"
                "- RouteVarName: str (Name of the route variable)\n"
                "- RouteVarShortName: str (Short name of the route variable)\n"
                "- RouteNo: str (Route number)\n"
                "- StartStop: str (Name of the starting stop)\n"
                "- EndStop: str (Name of the ending stop)\n"
                "- Distance: float (Distance of the route)\n"
                "- Outbound: bool (Indicates if the route is outbound)\n"
                "- RunningTime: float (Estimated running time of the route)\n",
                "parameters": {
                    "type_": "OBJECT",
                    "properties": {
                        "field": {"type_": "STRING"},
                        "value": {"type_": "STRING"},
                    },
                    "required": ["field", "value"],
                },
            },
            {
                "name": "pathsearch",
                "description": "Input query of (field, value) returns a list of path data with the following criteria:\n"
                "- lngs: list[float] (List of longitude coordinates)\n"
                "- lats: list[float] (List of latitude coordinates)\n"
                "- route: int (Route identifier)\n"
                "- var: int (Route variable identifier)\n",
                "parameters": {
                    "type_": "OBJECT",
                    "properties": {
                        "field": {"type_": "STRING"},
                        "value": {"type_": "STRING"},
                    },
                    "required": ["field", "value"],
                },
            },
        ]
    }
    model = genai.GenerativeModel(
        model_name="gemini-pro",
        tools=[funcs],
    )
    chat = model.start_chat()
    response = chat.send_message(qr)
    fc = response.candidates[0].content.parts[0].function_call
    f = fc.args["field"]
    v = fc.args["value"]
    if fc.name == "stopsearch":
        res = s.search(f, v)
        return res
    elif fc.name == "varsearch":
        res = r.search(f, v)
        return res
    elif fc.name == "pathsearch":
        res = p.search(f, v)
        return res
