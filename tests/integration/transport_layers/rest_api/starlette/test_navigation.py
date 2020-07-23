import starlette.testclient

from tests.integration import utils


def test_availability(
    test_client: starlette.testclient.TestClient,
    mock_service: utils.MockService,
) -> None:
    response = test_client.get("/")
    assert response.status_code == 200
