import pytest

from ufaas_dockerapi.client import DockerClient, default_transport


@pytest.fixture
async def client() -> DockerClient:  # NOTE: This fixture must be async.
    return DockerClient(default_transport())


@pytest.mark.asyncio
async def test_version(client):
    """
    Test a basic Docker API method, if this doesn't work something is really
    wrong.
    """
    res = await client.system.version()
    assert "Version" in res.keys()
