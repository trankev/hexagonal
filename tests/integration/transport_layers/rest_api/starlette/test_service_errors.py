from _pytest import logging
import pydantic
import pytest
import starlette.testclient

from hexagonal.models import ports
from tests.integration import utils

ERROR_MESSAGE = "internal message which shouldn't be leaked to response"


async def raise_exception(request: ports.Request[pydantic.BaseModel]) -> None:
    raise Exception(ERROR_MESSAGE)


def test_service_exception(
    mock_service: utils.MockService,
    test_client: starlette.testclient.TestClient,
    caplog: logging.LogCaptureFixture,
) -> None:
    with mock_service.with_behaviour(raise_exception):
        try:
            response = test_client.get("/unique")
        except Exception:
            pytest.fail("View shouldn't leak exceptions")
    assert response.status_code == 500
    body = response.json()
    assert len(body["messages"]) == 1
    message = body["messages"][0]
    assert message["severity"] == "error"
    assert message["code"] == "internal_error"
    assert ERROR_MESSAGE not in response.text

    assert any(record.exc_info for record in caplog.records)
