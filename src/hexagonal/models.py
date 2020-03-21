import enum
import logging
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


class MessageLevel(enum.IntEnum):
    trace = logging.DEBUG
    info = logging.INFO
    warning = logging.WARNING
    error = logging.ERROR
    fatal = logging.FATAL


class Message(pydantic.BaseModel):
    code: str
    level: int
    title: str
    source: typing.Optional[str]


class Response(pydantic.generics.GenericModel, typing.Generic[DataT, MetadataT]):
    data: DataT
    metadata: MetadataT
    messages: typing.Sequence[Message]
