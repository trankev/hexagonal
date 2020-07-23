import pytest
import starlette.applications
import starlette.testclient

from hexagonal import services
from hexagonal.transport_layers.rest_api import api
from hexagonal.transport_layers.rest_api import resources
from hexagonal.transport_layers.rest_api.starlette import routing


@pytest.fixture(name="rest_api", scope="session")
def rest_api_fixture(mock_service: services.ABBService) -> starlette.applications.Starlette:
    rest_api = api.API(
        resources=[
            resources.ResourceCollection(
                name="resources",
                list_service=mock_service,
                retrieve_service=mock_service,
                create_service=mock_service,
                update_service=mock_service,
            ),
            resources.UniqueResource(
                name="unique",
                retrieve_service=mock_service,
            ),
        ],
    )
    routes = routing.create_routes(rest_api)
    return starlette.applications.Starlette(debug=True, routes=routes)


@pytest.fixture(name="test_client", scope="session")
def test_client_fixture(rest_api: api.API) -> starlette.testclient.TestClient:
    return starlette.testclient.TestClient(rest_api)
