from src.models.Stop import Stop
from src.models.PathQuery import PathQuery
from src.utils.Cache import Cache
from src.models.RouteVarQuery import RouteVarQuery
from src.utils.helpers import calculate_distance


def dis():
    loc1 = (1, 40)
    loc2 = (2, 50)
    distance = calculate_distance(loc1, loc2)
    print(distance)


def main():
    r = RouteVarQuery().search(field="RouteId", value=1)
    print(r)


if __name__ == "__main__":
    dis()
