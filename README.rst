uFaaS Docker API
==================

:status: pre-alpha

An asyncio/aiohttp based Docker API.

In contrast to some other client libraries this one aims to offer:

* Async API.
* Configuration objects rather than JSON.
    - No camelcase keys.
    - Development environment friendly.
    - Makes usage more obvious.
* Object API in addition to a raw low-level Docker API.
* Python type hinting.
* Exec support, with WebSocket attachment.

Support for other parts of the Docker API such as Networking and Docker Swarm
support will be performed as uFaaS (eventually) requires them, or if patches
are submitted.

Basic Usage
------------
::

    from ufaas_dockerapi.client import DockerClient, default_transport
    from asyncio import get_event_loop

    loop = get_event_loop()
    client = DockerClient(default_transport())

    # View Docker system version info.
    loop.run_until_complete(client.system.version())

    # Pull alpine:3.8 from Docker Hub.
    loop.run_until_complete(client.image.pull("alpine", tag="3.8"))
