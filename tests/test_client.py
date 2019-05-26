from dataclasses import asdict

import pytest

from ufaas_dockerapi.client import DockerClient, default_transport
from ufaas_dockerapi.config import (ContainerConfig, ExecConfig,
                                    config_dict_factory)


@pytest.fixture
async def client() -> DockerClient:  # NOTE: This fixture must be async.
    return DockerClient(default_transport())


@pytest.fixture
async def alpine(client) -> None:
    """
    Ensure Alpine image is available.
    """
    await client.image.pull("alpine", tag="3.8")  # 3.8 is small.


@pytest.fixture
async def alpine_container(client, alpine) -> None:
    """
    Alpine container created, but not started.
    """
    config = {
        "image": "alpine:3.8",
        "cmd": ["/bin/ash"],
        "tty": False,
        "attach_stdin": True,
        "attach_stdout": True,
        "attach_stderr": True,
        "open_stdin": True,
        "stdin_once": True
        }

    try:
        await client.container.delete("alpine_container", force_stop=True)
    except Exception:
        pass

    await client.container.create(
            "alpine_container", ContainerConfig(**config)
            )


@pytest.fixture
async def alpine_container_started(client, alpine_container) -> None:
    await client.container.start("alpine_container")


@pytest.mark.asyncio
async def test_version(client):
    """
    Test a basic Docker API method, if this doesn't work something is really
    wrong.
    """
    _, res = await client.system.version()
    assert "ApiVersion" in res.keys()


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
        await client.image.remove("alpine:3.8", force=True)
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
async def test_container_basic(client, alpine):
    """
    Test minimal container create and delete, requires an image creation too.
    """
    basic_config = ContainerConfig(**{
        "image": "alpine:3.8"
    })

    try:
        await client.container.create("test_container", basic_config)
    except Exception as e:
        pytest.fail("Creating container with alpine:3.8 failed: %s" % e)

    try:
        await client.container.delete("test_container", force_stop=True)
    except Exception as e:
        pytest.fail("Deleting 'test_container' failed: %s" % e)


@pytest.mark.asyncio
async def test_exec(client, alpine_container_started):
    """
    Test that an exec instance can be created and runs
    """
    exec_config = ExecConfig(**{
        "cmd": ["echo", "hello world"],
        "tty": True
    })

    try:
        status, _ = await client.exec.run("alpine_container", exec_config)
        assert status == 200
    except Exception as e:
        pytest.fail("Exec test failed: %s" % e)


@pytest.mark.asyncio
async def test_websocket(client, alpine_container_started):
    """
    See if "hello world" is returned over websocket when echo "hello world" is
    run.
    """

    ws_config = {
        "return_stream": True,
        "attach_stdout": True,
        "attach_stderr": True,
        "attach_stdin": True
    }

    ws = await client.container.attach_websocket("alpine_container",
                                                 **ws_config)

    await ws.send_str('echo "hello world"\n')
    output = await ws.receive()

    assert "hello world" in "{}".format(output)
    await ws.close()
