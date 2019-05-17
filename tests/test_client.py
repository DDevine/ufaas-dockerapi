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


@pytest.mark.asyncio
async def test_image_basics(client):
    """
    Pull an image from Dockerhub.
    """
    try:
        await client.image.pull("alpine", tag="3.8")  # 3.8 is small.
    except Exception as e:
        pytest.fail("Pulling image 'alpine:3.8' failed: %s" % e)

    try:
        await client.image.remove("alpine:3.8")
    except Exception as e:
        pytest.fail("Removing image 'alpine:3.8' failed: %s" % e)
