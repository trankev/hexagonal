import pydantic
import pytest
import starlette.applications
import starlette.testclient

from hexagonal import services
from hexagonal.models import ports
from hexagonal.transport_layers.rest_api import api
from hexagonal.transport_layers.rest_api import resources
from hexagonal.transport_layers.rest_api.starlette import routing


class Data(pydantic.BaseModel):
    int_field: int
    bool_field: bool


class ResourceListingService(services.ABBService[ports.Listing[Data]]):
    name = "list_resource"

    data = [
        Data(int_field=5, bool_field=True),
        Data(int_field=3, bool_field=False),
    ]

    async def run(self, request: ports.Request[ports.NoParams]) -> ports.Response[dict]:
        response = ports.Response(
            data=ports.Listing(items=self.data),
            messages=[],
        )
        return response


@pytest.fixture(name="rest_api", scope="session")
def rest_api_fixture() -> starlette.applications.Starlette:
    rest_api = api.API(
        resources=[
            resources.Resource(
                name="resources",
                list_service=ResourceListingService(),
            ),
        ],
    )
    routes = routing.create_routes(rest_api)
    return starlette.applications.Starlette(debug=True, routes=routes)


@pytest.fixture(name="test_client", scope="session")
def test_client_fixture(rest_api: api.API) -> starlette.testclient.TestClient:
    return starlette.testclient.TestClient(rest_api)


def test_list_resource(test_client: starlette.testclient.TestClient) -> None:
    response = test_client.get("/resources")
    assert response.status_code == 200
    expected = {
        "data": {
            "items": [item.dict() for item in ResourceListingService.data],
        },
        "messages": [],
    }

    assert response.json() == expected
