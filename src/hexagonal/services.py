import abc
import typing

import pydantic

from hexagonal.models import ports
from hexagonal.transport_layers.rest_api import mappings

DataT = typing.TypeVar("DataT", bound=pydantic.BaseModel)


class Service(abc.ABC):
    name: typing.ClassVar[str]
    rest_api_mapping: typing.Tuple[mappings.Mapping, ...] = ()

    RequestClass: typing.Any = ports.NoParams  # subclasses as attribute not supported


class ABBService(Service, abc.ABC, typing.Generic[DataT]):
    """Asynchronous Basic request, basic response interactor."""

    async def run(
        self,
        request: ports.Request[Service.RequestClass],
    ) -> ports.Response[DataT]:
        raise NotImplementedError()
