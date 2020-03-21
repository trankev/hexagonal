import dataclasses
import typing

from hexagonal.transport_layers.rest_api import resources


@dataclasses.dataclass
class API:
    resources: typing.Sequence[resources.Resource]
