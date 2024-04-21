from src.models.RouteVarQuery import RouteVarQuery
from src.models.StopQuery import StopQuery
from src.models.Stop import Stop

from src.models.Graph import Graph

# from src.models.Graph import Graph
from src.models.Path import Path
from src.utils.Cache import Cache
from src.utils.constants import ROUTEVAR_STOP_MAP, STOP_LIST, VAR_LIST
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


# def test_var_stop_map():
#     # stops: list = Stop.load_stop()
#     paths = Path.load_path()
#     # RouteVar.load_route_var()
#     stop_on_route = Cache.get(ROUTEVAR_STOP_MAP)[(1, 1)]
#     path_on_route = paths[(1, 1)]
#
#     stop_map = []
#
#     route = geojson.LineString(path_on_route.lng_lat_list)
#     feature = geojson.Feature(geometry=route, properties={"RouteId": 1})
#     collection = []
#     collection.append(feature)
#
#     from src.utils.helpers import calculate_distance, distance_finder
#
#     df = distance_finder((1, 1))
#     prev = stop_on_route[0]
#     stop = stops[prev]
#     stop_map.append(
#         (stop.Lng, stop.Lat),
#     )
#     total_distance = 0
#     for stop in stop_on_route[1:]:
#         stop = stops[stop]
#         stop_map.append(
#             (stop.Lng, stop.Lat),
#         )
#         dis, _ = df(prev, stop.StopId)
#         total_distance += dis
#
#     stop_map = geojson.Feature(geometry=geojson.MultiPoint(stop_map))
#     collection.append(stop_map)
#     print(total_distance)
#
#     with open("demo/stop_map.geojson", "w") as file:
#         file.write(str(geojson.FeatureCollection(collection)))


def test_graph2():
    Stop.load_stop()
    Path.load_path()
    g = Graph()
    # g.find_shortest_paths()
    g.export_path(1, 7266)


def search_route():
    q = RouteVarQuery()
    q.search("RouteId", 1)


def main():
    search_route()


if __name__ == "__main__":
    main()
