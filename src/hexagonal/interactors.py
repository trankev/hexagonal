import abc
import typing

import pydantic

from hexagonal import models


DataT = typing.TypeVar("DataT")
MetadataT = typing.TypeVar("MetadataT")


class NoParams(pydantic.BaseModel):
    pass


class Interactor(abc.ABC):
    name: typing.ClassVar[str]
    rest_api_mapping = ()
    RequestClass: typing.ClassVar[typing.Type[pydantic.BaseModel]] = NoParams


class BRBRInteractor(Interactor, abc.ABC, typing.Generic[DataT, MetadataT]):
    """Basic request, basic response interactor."""

    async def run(
        self,
        request: models.Request[Interactor.RequestClass],
    ) -> models.Response[DataT, MetadataT]:
        raise NotImplementedError()
