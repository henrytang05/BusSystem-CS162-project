import pandas as pd
import ast
from shapely.geometry import LineString, mapping
from geojson import Feature, FeatureCollection


def export_geojson(start=210, end=439):
    dtype = {"src": "int32", "des": "int32", "time": "float128", "path": "str"}
    df = pd.read_csv(f"output/shortest_path/{start}.csv", dtype=dtype)
    filtered_df = df[df["des"] == end]

    # Extract the path value from the Series and convert it to a list of tuples
    path_value = filtered_df["path"].iloc[0]
    path_list = ast.literal_eval(path_value)

    # Now you can work with the list of tuples representing coordinates

    line = LineString(path_list)
    feature = Feature(geometry=mapping(line))
    features_collection = []
    features_collection.append(feature)
    #
    with open("output/path1.geojson", "w") as file:
        file.write(str(FeatureCollection(features_collection)))


#
#
export_geojson()
