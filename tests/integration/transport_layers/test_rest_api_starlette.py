import pytest
import starlette.applications
import starlette.testclient

from hexagonal import services
from hexagonal.transport_layers.rest_api import api
from hexagonal.transport_layers.rest_api import resources
from hexagonal.transport_layers.rest_api.starlette import routing
from tests.integration import utils


@pytest.fixture(name="rest_api", scope="session")
def rest_api_fixture(mock_service: services.ABBService) -> starlette.applications.Starlette:
    rest_api = api.API(
        resources=[
            resources.Resource(
                name="resources",
                list_service=mock_service,
            ),
        ],
    )
    routes = routing.create_routes(rest_api)
    return starlette.applications.Starlette(debug=True, routes=routes)


@pytest.fixture(name="test_client", scope="session")
def test_client_fixture(rest_api: api.API) -> starlette.testclient.TestClient:
    return starlette.testclient.TestClient(rest_api)


def test_nominal(
    test_client: starlette.testclient.TestClient,
    mock_service: utils.MockService,
) -> None:
    response = test_client.get("/resources")
    assert response.status_code == 200
    expected = mock_service.response().json()

    assert response.text == expected
