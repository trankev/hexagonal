import pytest
import starlette.applications
import starlette.testclient

from hexagonal import interactors
from hexagonal import models
from hexagonal.transport_layers.rest_api import api
from hexagonal.transport_layers.rest_api import resources
from hexagonal.transport_layers.rest_api.starlette import routing


class ResourceListingInteractor(interactors.BRBRInteractor[dict, dict]):
    name = "list_resource"

    data = [
        {
            "id": 1,
            "version": 10,
            "attributes": {
                "int_field": 5,
                "bool_field": True,
            },
        },
        {
            "id": 2,
            "version": 3,
            "attributes": {
                "int_field": 3,
                "bool_field": False,
            },
        },
    ]

    async def run(self, request: models.Request[models.NoParams]) -> models.Response[dict, dict]:
        return models.Response(
            data=self.data,
            metadata={},
            messages=[],
        )


@pytest.fixture(name="rest_api", scope="session")
def rest_api_fixture() -> starlette.applications.Starlette:
    rest_api = api.API(
        resources=[
            resources.Resource(
                name="resources",
                list_interactor=ResourceListingInteractor(),
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
        "data": ResourceListingInteractor.data,
        "metadata": {},
        "messages": [],
    }

    assert response.json() == expected
