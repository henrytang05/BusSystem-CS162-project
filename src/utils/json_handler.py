__all__ = ["loader"]

import json
from typing import Generator


def loader(filename: str) -> Generator:
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            yield json.loads(line)


def writer(filename: str, data: list) -> None:
    if not data:
        with open(filename, "w", encoding="utf-8") as file:
            file.write("Not Found")
            return
    with open(filename, "w"):
        pass
    with open(filename, "a", encoding="utf8") as file:
        for item in data:
            obj: str = json.dumps(item.__dict__, ensure_ascii=False)
            file.write(obj + "\n")
