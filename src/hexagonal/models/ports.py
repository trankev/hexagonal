import typing

import pydantic
import pydantic.generics

from hexagonal.models import messages as messages_module

DataT = typing.TypeVar("DataT", bound=pydantic.BaseModel)
ItemT = typing.TypeVar("ItemT", bound=pydantic.BaseModel)
ParamsT = typing.TypeVar("ParamsT", bound=pydantic.BaseModel)


class Response(pydantic.generics.GenericModel, typing.Generic[DataT]):
    data: typing.Union[DataT, None]
    messages: typing.Sequence[messages_module.Message] = pydantic.Field(default_factory=list)


class Request(pydantic.generics.GenericModel, typing.Generic[ParamsT]):
    params: ParamsT


class NoParams(pydantic.BaseModel):
    pass


class Listing(pydantic.BaseModel, typing.Generic[ItemT]):
    items: typing.List[ItemT]


class Link(pydantic.BaseModel):
    href: str
    name: str


class Error(Exception):

    def __init__(self, messages: messages_module.Message):
        self.messages = messages
