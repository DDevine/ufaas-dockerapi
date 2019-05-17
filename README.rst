uFaaS Docker API
==================

:status: pre-alpha

An asyncio/aiohttp based docker API client targeted at uFaaS use-cases.
The official docker python API is not used because it is not async, and `aiodocker` is
not used because it lacks `exec` support which is critical.

Setting labels will also be supported, as it is likely important to uFaaS.

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
