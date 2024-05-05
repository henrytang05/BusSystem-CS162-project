from typing import Type


class Query:
    def __init__(self, field, value) -> None:
        self.field = field
        self.value = value

    def is_valid(self, class_name: Type) -> bool:
        if self.field not in class_name.__annotations__.keys():
            return False
        field_type = class_name.__annotations__[self.field]
        try:
            field_type = eval(field_type)
        except NameError:
            return False
        if not isinstance(self.value, field_type):
            try:
                self.value = field_type(self.value)
            except (ValueError, TypeError):
                return False
        return True
