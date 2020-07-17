import enum
import logging
import typing

import pydantic
import pydantic.generics

DataT = typing.TypeVar("DataT", bound=pydantic.BaseModel)
ItemT = typing.TypeVar("ItemT", bound=pydantic.BaseModel)
ParamsT = typing.TypeVar("ParamsT", bound=pydantic.BaseModel)


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


class Response(pydantic.generics.GenericModel, typing.Generic[DataT]):
    data: DataT
    messages: typing.Sequence[Message]


class Request(pydantic.generics.GenericModel, typing.Generic[ParamsT]):
    params: ParamsT


class NoParams(pydantic.BaseModel):
    pass


class Listing(pydantic.BaseModel, typing.Generic[ItemT]):
    items: typing.List[ItemT]
