import abc
import typing

import pydantic

from hexagonal import models

DataT = typing.TypeVar("DataT", bound=pydantic.BaseModel)


class Service(abc.ABC):
    name: typing.ClassVar[str]
    rest_api_mapping = ()

    RequestClass: typing.Any = models.NoParams  # subclasses as attribute not supported


class ABBService(Service, abc.ABC, typing.Generic[DataT]):
    """Asynchronous Basic request, basic response interactor."""

    async def run(
        self,
        request: models.Request[Service.RequestClass],
    ) -> models.Response[DataT]:
        raise NotImplementedError()
