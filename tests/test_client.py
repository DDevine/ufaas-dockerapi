from dataclasses import asdict

import pytest

from ufaas_dockerapi.client import DockerClient, default_transport
from ufaas_dockerapi.config import ContainerConfig, config_dict_factory


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
    Test create (pulling alpine from Dockerhub) and deletion of an image.
    """
    try:
        await client.image.pull("alpine", tag="3.8")  # 3.8 is small.
    except Exception as e:
        pytest.fail("Pulling image 'alpine:3.8' failed: %s" % e)

    try:
        await client.image.remove("alpine:3.8")
    except Exception as e:
        pytest.fail("Removing image 'alpine:3.8' failed: %s" % e)


@pytest.mark.asyncio
async def test_config_serialisation():
    """
    Test creation of basic config objects, and that they serialise to JSON.
    """
    config = ContainerConfig({
        "image": "alpine:3.8"
    })

    try:
        asdict(config, dict_factory=config_dict_factory)
    except Exception as e:
        pytest.fail("Config object serialisation failed: %s" % e)


@pytest.mark.asyncio
async def test_container_basic(client):
    """
    Test minimal container create and delete, requires an image creation too.
    """
    basic_config = ContainerConfig(**{
        "image": "alpine:3.8"
    })

    try:
        await client.image.pull("alpine", tag="3.8")  # 3.8 is small.
    except Exception as e:
        pytest.fail("Pull of 'alpine:3.8' for container test failed: %s" % e)

    try:
        await client.container.create("test_container", basic_config)
    except Exception as e:
        pytest.fail("Creating container with alpine:3.8 failed: %s" % e)

    try:
        await client.container.delete("test_container", force_stop=True)
    except Exception as e:
        pytest.fail("Deleting 'test_container' failed: %s" % e)
