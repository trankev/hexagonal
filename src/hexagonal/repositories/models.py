import dataclasses
import enum


class SortDirection(enum.Enum):
    ascending = enum.auto()
    descending = enum.auto()


@dataclasses.dataclass
class SortOption:
    field: str
    direction: SortDirection
