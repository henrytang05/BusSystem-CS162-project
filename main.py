from src.models.RouteVarQuery import RouteVarQuery
from src.models.StopQuery import StopQuery
from src.models.Stop import Stop

# from src.models.Graph import Graph
from src.models.Path import Path
from src.models.RouteVar import RouteVar
from src.utils.Cache import Cache
from src.utils.constants import *
from pyproj import Proj
import geojson
import colorsys
import json


def generate_rainbow_colors(num_colors):
    colors = []
    for i in range(num_colors):
        hue = 360.0 * i / num_colors
        rgb = colorsys.hsv_to_rgb(hue / 360.0, 1.0, 1.0)
        color = "#{:02x}{:02x}{:02x}".format(
            int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
        )
        colors.append(color)
    return colors


def test_geojson():
    RouteVar.load_route_var()

    paths = Cache.get(VAR_LIST)

    # Generate rainbow colors
    num_colors = len(paths)
    rainbow_colors = generate_rainbow_colors(num_colors)
    features = []
    for index, path in enumerate(paths):
        lines = geojson.LineString(path.lng_lat_list)
        f = geojson.Feature(
            geometry=lines,
            properties={
                "RouteId": path.RouteId,
                "RouteVarId": path.RouteVarId,
                "fill": rainbow_colors[index],
                "stroke": rainbow_colors[index],
            },
        )
        features.append(f)

    collection = geojson.FeatureCollection(features)

    with open("tmp.geojson", "w") as file:
        file.write(str(collection))


def test_var_stop_map():
    from src.models.PathQuery import PathQuery
    from src.models.Stop import Stop

    RouteVar.load_route_var()
    Stop.load_stop()
    lines = []
    stops = Cache.get(ROUTEVAR_STOP_MAP)[
        RouteVarQuery().search(field="RouteNo", value="03")[1]
    ]
    num_colors = len(stops)
    rainbow_colors = generate_rainbow_colors(num_colors)
    last = stops[0]
    for index, stop in enumerate(stops[1:]):
        loc = [[last.Lng, last.Lat], [stop.Lng, stop.Lat]]
        line = geojson.LineString(loc)
        f = geojson.Feature(
            geometry=line,
            properties={
                "fill": rainbow_colors[index],
                "stroke": rainbow_colors[index],
            },
        )
        lines.append(f)
        last = stop

    collection = geojson.FeatureCollection(lines)

    with open("tmp.geojson", "w") as file:
        file.write(str(collection))


def test_graph2():
    from src.models.Graph2 import Graph

    Stop.load_stop()
    g = Graph()
    res = g.find_shortest_path()
    g.output_as_json(res)


def main():
    test_graph2()


if __name__ == "__main__":
    main()
