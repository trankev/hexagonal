import contextlib
import copy
import typing

import pydantic

from hexagonal import services
from hexagonal.models import messages
from hexagonal.models import ports
from hexagonal.transport_layers.rest_api import mappings


async def do_nothing(request: ports.Request[pydantic.BaseModel]) -> None:
    pass


Behaviour = typing.Callable[[ports.Request[pydantic.BaseModel]], typing.Awaitable[None]]

DEFAULT_MESSAGES: typing.List[messages.Message] = []


class Data(pydantic.BaseModel):
    int_field: int = 12
    bool_field: bool = False


class MockService(services.ABBService[Data]):
    name = "mock_service"

    def __init__(self) -> None:
        self.return_data = Data()
        self.messages: typing.List[messages.Message] = DEFAULT_MESSAGES
        self.behaviour: Behaviour = do_nothing

    async def run(self, request: ports.Request[ports.NoParams]) -> ports.Response[dict]:
        await self.behaviour(request)
        response = self.response()
        return response

    def response(self) -> ports.Response:
        response = ports.Response(
            data=copy.deepcopy(self.return_data),
            messages=copy.deepcopy(self.messages),
        )
        return response

    @contextlib.contextmanager
    def custom_behaviour(self, behaviour: Behaviour) -> typing.Iterator[None]:
        self.behaviour = behaviour
        try:
            yield
        finally:
            self.behaviour = do_nothing

    @contextlib.contextmanager
    def custom_messages(self, messages: typing.List[messages.Message]) -> typing.Iterator[None]:
        self.messages = messages
        try:
            yield
        finally:
            self.messages = DEFAULT_MESSAGES

    @contextlib.contextmanager
    def custom_request(
        self,
        request_cls: typing.Type[pydantic.BaseModel],
        mapping: typing.Tuple[mappings.Mapping, ...],
    ) -> typing.Iterator[None]:
        self.RequestClass = request_cls
        self.rest_api_mapping = mapping
        try:
            yield
        finally:
            self.RequestClass = ports.NoParams
            self.rest_api_mapping = ()
