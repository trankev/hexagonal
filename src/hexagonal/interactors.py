import abc
import typing

from hexagonal import models


DataT = typing.TypeVar("DataT")
MetadataT = typing.TypeVar("MetadataT")


class Interactor(abc.ABC, typing.Generic[DataT, MetadataT]):
    name: typing.ClassVar[str]

    async def run(self) -> models.Response[DataT, MetadataT]:
        raise NotImplementedError()
