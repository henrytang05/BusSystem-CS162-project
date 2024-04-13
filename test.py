from src.models.Stop import Stop
from src.models.PathQuery import PathQuery
from src.utils.Cache import Cache


def main():
    Stop.load_stop()
    not_found = []
    for id, stop in Cache.get("Stop List").items():
        lat = stop.Lat
        lng = stop.Lng

        res, wp = PathQuery().search(field="lng_lat_list", value=(lng, lat))
        if not res:
            print("Not found", id, wp)
            not_found.append(id)

        # else:
        #     print("Found", id)


if __name__ == "__main__":
    main()
