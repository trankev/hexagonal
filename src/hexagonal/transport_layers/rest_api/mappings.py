import enum

import pydantic


@enum.unique
class Source(enum.Enum):
    header = enum.auto()
    path = enum.auto()
    query = enum.auto()
    body = enum.auto()


class Mapping(pydantic.BaseModel):
    attribute: str
    source: Source
    field: str
