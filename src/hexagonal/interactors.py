import abc
import typing

import pydantic

from hexagonal import models


DataT = typing.TypeVar("DataT", bound=pydantic.BaseModel)
MetadataT = typing.TypeVar("MetadataT", bound=pydantic.BaseModel)


class Interactor(abc.ABC):
    name: typing.ClassVar[str]
    rest_api_mapping = ()

    RequestClass: typing.Any = models.NoParams  # subclasses as attribute not supported


class BRBRInteractor(Interactor, abc.ABC, typing.Generic[DataT, MetadataT]):
    """Basic request, basic response interactor."""

    async def run(
        self,
        request: models.Request[Interactor.RequestClass],
    ) -> models.Response[DataT, MetadataT]:
        raise NotImplementedError()
