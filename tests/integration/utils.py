import copy
import typing

import pydantic

from hexagonal import services
from hexagonal.models import messages
from hexagonal.models import ports


class Data(pydantic.BaseModel):
    int_field: int = 12
    bool_field: bool = False


class MockService(services.ABBService[Data]):
    name = "mock_service"

    def __init__(self) -> None:
        self.return_data = Data()
        self.messages: typing.List[messages.Message] = []

    async def run(self, request: ports.Request[ports.NoParams]) -> ports.Response[dict]:
        return self.response()

    def response(self) -> ports.Response:
        response = ports.Response(
            data=copy.deepcopy(self.return_data),
            messages=copy.deepcopy(self.messages),
        )
        return response
