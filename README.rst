uFaaS Docker API
==================
An asyncio/aiohttp based docker API client targeted at uFaaS use-cases.
The official docker python API is not used because it is not async, and `aiodocker` is
not used because it lacks `exec` support which is critical.

Setting labels will also be supported, as it is likely important to uFaaS.