import enum
import logging
import typing

import pydantic
import pydantic.generics


DataT = typing.TypeVar("DataT")
MetadataT = typing.TypeVar("MetadataT")
ParamsT = typing.TypeVar("ParamsT")


class MessageLevel(enum.IntEnum):
    trace = logging.DEBUG
    info = logging.INFO
    warning = logging.WARNING
    error = logging.ERROR
    fatal = logging.FATAL


class Message(pydantic.BaseModel):
    code: str
    severity: int
    title: str
    source: typing.Optional[str]


class Response(pydantic.generics.GenericModel, typing.Generic[DataT, MetadataT]):
    data: DataT
    metadata: MetadataT
    messages: typing.Sequence[Message]


class Request(pydantic.generics.GenericModel, typing.Generic[ParamsT]):
    params: ParamsT
