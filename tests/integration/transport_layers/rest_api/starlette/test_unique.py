import pytest
import starlette.testclient

from tests.integration import utils


@pytest.mark.parametrize(
    ("path", "method", "expected_status"),
    (("/unique", "GET", 200), ),
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
