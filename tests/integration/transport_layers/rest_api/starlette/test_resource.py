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
                retrieve_service=mock_service,
                create_service=mock_service,
                update_service=mock_service,
            ),
        ],
    )
    routes = routing.create_routes(rest_api)
    return starlette.applications.Starlette(debug=True, routes=routes)


@pytest.fixture(name="test_client", scope="session")
def test_client_fixture(rest_api: api.API) -> starlette.testclient.TestClient:
    return starlette.testclient.TestClient(rest_api)


@pytest.mark.parametrize(
    ("path", "method", "expected_status"),
    (
        ("/resources", "GET", 200),
        ("/resources", "POST", 201),
        ("/resources/some_id", "GET", 200),
        ("/resources/some_id", "PUT", 200),
    ),
)
def test_availability(
    test_client: starlette.testclient.TestClient,
    mock_service: utils.MockService,
    path: str,
    method: str,
    expected_status: int,
) -> None:
    response = test_client.request(method, path)
    assert response.status_code == expected_status
    expected = mock_service.response().json()

    assert response.text == expected
