import uuid

from _pytest import logging
import pydantic
import pytest
import starlette.testclient

from hexagonal.models import messages
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
    with mock_service.custom_behaviour(raise_exception):
        response = test_client.get("/unique")
    assert response.status_code == 500
    body = response.json()
    assert len(body["messages"]) == 1
    message = body["messages"][0]
    assert message["severity"] == "error"
    assert message["code"] == "internal_error"
    assert ERROR_MESSAGE not in response.text

    assert any(record.exc_info for record in caplog.records)


@pytest.mark.parametrize(
    ("message", "expected_status_code"),
    (
        (messages.field_error("", ""), 400),
        (messages.resource_not_found("", uuid.uuid4()), 404),
        (messages.outdated_resource("", uuid.uuid4(), 1, 2), 412),
        (messages.internal_error(), 500),
        *(
            (
                messages.Message(
                    code=messages.ErrorCode.miscellanous,
                    severity=message_level,
                    title="",
                    source=None,
                ),
                200,
            ) for message_level in (
                messages.MessageLevel.warning,
                messages.MessageLevel.info,
                messages.MessageLevel.trace,
            )
        ),
        *(
            (
                messages.Message(
                    code=messages.ErrorCode.miscellanous,
                    severity=message_level,
                    title="",
                    source=None,
                ),
                500,
            ) for message_level in (
                messages.MessageLevel.error,
                messages.MessageLevel.fatal,
            )
        ),
    ),
)
def test_error_code_conversion(
    mock_service: utils.MockService,
    test_client: starlette.testclient.TestClient,
    message: messages.Message,
    expected_status_code: int,
) -> None:
    with mock_service.custom_messages([message]):
        response = test_client.get("/unique")
    assert response.status_code == expected_status_code
