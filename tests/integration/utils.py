import contextlib
import copy
import typing

import pydantic

from hexagonal import services
from hexagonal.models import messages
from hexagonal.models import ports


async def do_nothing(request: ports.Request[pydantic.BaseModel]) -> None:
    pass


Behaviour = typing.Callable[[ports.Request[pydantic.BaseModel]], typing.Awaitable[None]]


class Data(pydantic.BaseModel):
    int_field: int = 12
    bool_field: bool = False


class MockService(services.ABBService[Data]):
    name = "mock_service"

    def __init__(self) -> None:
        self.return_data = Data()
        self.messages: typing.List[messages.Message] = []
        self.behaviour: Behaviour = do_nothing

    async def run(self, request: ports.Request[ports.NoParams]) -> ports.Response[dict]:
        await self.behaviour(request)
        return self.response()

    def response(self) -> ports.Response:
        response = ports.Response(
            data=copy.deepcopy(self.return_data),
            messages=copy.deepcopy(self.messages),
        )
        return response

    @contextlib.contextmanager
    def with_behaviour(self, behaviour: Behaviour) -> typing.Iterator[None]:
        self.behaviour = behaviour
        yield
        self.behaviour = do_nothing
