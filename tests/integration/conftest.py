import pytest

from tests.integration import utils


@pytest.fixture(name="mock_service", scope="session")
def mock_service_fixture() -> utils.MockService:
    return utils.MockService()
