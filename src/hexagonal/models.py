import enum
import typing

import pydantic
import pydantic.generics


AttributesT = typing.TypeVar("AttributesT")


class Resource(pydantic.generics.GenericModel, typing.Generic[AttributesT]):
    id: str
    version: typing.Optional[int]
    attributes: AttributesT


DataT = typing.TypeVar("DataT")
MetadataT = typing.TypeVar("MetadataT")


class MessageLevel(enum.Enum):
    trace = enum.auto()
    info = enum.auto()
    warning = enum.auto()
    error = enum.auto()
    fatal = enum.auto()


class Message(pydantic.BaseModel):
    code: str
    level: MessageLevel
    title: str
    source: typing.Optional[str]


class Response(pydantic.generics.GenericModel, typing.Generic[DataT, MetadataT]):
    data: DataT
    metadata: MetadataT
    messages: typing.Sequence[Message]
