# Technical Report for CS162 Project

# WO6

## Added Models

The data models for (`Path`) represent a path associated with a RouteId and RouteVarId, the path is represented in a list of longitute_latitute pair

The query class (`PathQuery`) provide methods for search for a particular path based on the field and value, a method to output the value into csv and json format

## Discovery tasks

Learned about geojson, pyproj, shapely and rtree
Found some LLM library to choose method based on query

## Project Structure

The project is organized into several directories:

- `src/`: Contains the source code for the project.
- `src/models/`: Contains the data models used in the project, including `RouteVar`, `RouteVarQuery`, `Stop`, and `StopQuery`.
- `src/utils/`: Contains utility functions and classes, including `Cache`, `helpers`, and `json_handler`.
- `tests/`: Contains unit tests for the various components of the project.
- `data/`: Contains data files used in the project.
- `query/`: Contains query results.
- `Diagrams/`: Contains diagrams for the project.

## Key Components

### Data Models

The data models (`RouteVar` and `Stop`) represent the core data structures used in the project. They encapsulate the properties of a route and a stop, respectively.

### Query Classes

The query classes (`RouteVarQuery` and `StopQuery`) provide methods for querying the data models. They use the `Cache` class to store and retrieve data.

### Utility Classes

The utility classes include `Cache`, which provides a caching mechanism for the data models, and `helpers` and `json_handler`, which provide various utility functions.

## Testing

The project includes a suite of unit tests located in the `tests/` directory. These tests cover the data models, query classes, and utility functions.

## Running the Project

`pip install -r requirements.txt`
`python main.py`


