import abc
import typing

from hexagonal import models


DataT = typing.TypeVar("DataT")
MetadataT = typing.TypeVar("MetadataT")


class Interactor(abc.ABC):
    name: typing.ClassVar[str]


class BRBRInteractor(Interactor, abc.ABC, typing.Generic[DataT, MetadataT]):
    """Basic request, basic response interactor."""

    async def run(self) -> models.Response[DataT, MetadataT]:
        raise NotImplementedError()
