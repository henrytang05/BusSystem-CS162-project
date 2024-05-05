import pandas as pd
import ast
from shapely.geometry import LineString, mapping
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

def find_a
def main():
    export_geojson()


main()
