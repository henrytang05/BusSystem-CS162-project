import os

__all__ = (
    "CWD",
    "PATH_FILE",
    "STOP_FILE",
    "VAR_FILE",
    "VAR_LIST",
    "VAR_SEARCH_RESULT",
    "PATH_LIST",
    "PATH_SEARCH_RESULTS",
    "STOP_LIST",
    "ROUTEVAR_STOP_MAP",
    "STOP_SEARCH_RESULTS",
    "SHORTEST_PATHS",
)

CWD = os.getcwd()
PATH_FILE = f"{CWD}/data/paths.json"
STOP_FILE = f"{CWD}/data/stops.json"
VAR_FILE = f"{CWD}/data/vars.json"

# Cached values
VAR_LIST = "VAR_LIST"  # access through (RouteId, RouteVarId)
STOP_LIST = "Stop List"  # access through StopId
VAR_SEARCH_RESULT = "VAR SEARCH RESULT"  # access through (field, value)
PATH_LIST = "Path List"  # access through (RouteId, RouteVarId)
PATH_SEARCH_RESULTS = "Path Search Results"
ROUTEVAR_STOP_MAP = "Route Stop Map"  # access through (RouteId, RouteVarId), dict[(RouteId, RouteVarId), list[StopId]]
STOP_SEARCH_RESULTS = "Stop Search Results"
SHORTEST_PATHS = "Shortest Paths"
