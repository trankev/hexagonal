import typing

import pydantic
import pydantic.generics

from hexagonal.models import messages

DataT = typing.TypeVar("DataT", bound=pydantic.BaseModel)
ItemT = typing.TypeVar("ItemT", bound=pydantic.BaseModel)
ParamsT = typing.TypeVar("ParamsT", bound=pydantic.BaseModel)


class Response(pydantic.generics.GenericModel, typing.Generic[DataT]):
    data: typing.Union[DataT, None]
    messages: typing.Sequence[messages.Message]


class Request(pydantic.generics.GenericModel, typing.Generic[ParamsT]):
    params: ParamsT


class NoParams(pydantic.BaseModel):
    pass


class Listing(pydantic.BaseModel, typing.Generic[ItemT]):
    items: typing.List[ItemT]
