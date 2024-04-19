from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Query:
    field: str
    value: Any

    def is_valid(self, class_name: str, field: str) -> bool:
        if field not in class_name.__annotations__.keys():
            return False
        return True
