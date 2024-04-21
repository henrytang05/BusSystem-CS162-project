from dataclasses import dataclass
from typing import Any, Type


@dataclass(frozen=True)
class Query:
    field: str
    value: Any

    def is_valid(self, class_name: Type) -> bool:
        if self.field not in class_name.__annotations__.keys():
            return False
        return True
