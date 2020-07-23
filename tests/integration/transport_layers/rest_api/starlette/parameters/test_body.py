import typing

import pydantic
import pytest
import starlette.testclient

from hexagonal.models import ports
from hexagonal.transport_layers.rest_api import mappings
from tests.integration import utils


class IntParameter(pydantic.BaseModel):
    int_field: int


SAMPLE_VALUE = 144


async def validate_parameter(request: ports.Request[IntParameter]) -> None:
    assert request.params.int_field == SAMPLE_VALUE


@pytest.fixture(name="body_parameter", scope="module")
def body_parameter_fixture(mock_service: utils.MockService) -> typing.Iterator[None]:
    custom_request = mock_service.custom_request(
        IntParameter,
        (
            mappings.Mapping(
                attribute="int_field",
                source=mappings.Source.body,
                field="int_field",
            ),
        ),
    )

    custom_behaviour = mock_service.custom_behaviour(validate_parameter)
    with custom_request, custom_behaviour:
        yield


@pytest.mark.usefixtures("body_parameter")
def test_nominal(test_client: starlette.testclient.TestClient) -> None:
    response = test_client.get("/unique", json={"int_field": SAMPLE_VALUE})
    assert response.status_code == 200


@pytest.mark.usefixtures("body_parameter")
def test_missing(test_client: starlette.testclient.TestClient) -> None:
    response = test_client.get("/unique")
    assert response.status_code == 400
    body = response.json()
    assert any(message["code"] == "missing_field" for message in body["messages"])


@pytest.mark.usefixtures("body_parameter")
def test_wrong_type(test_client: starlette.testclient.TestClient) -> None:
    response = test_client.get("/unique", json={"int_field": "not an int"})
    assert response.status_code == 400
    body = response.json()
    assert any(message["code"] == "input_error" for message in body["messages"])
