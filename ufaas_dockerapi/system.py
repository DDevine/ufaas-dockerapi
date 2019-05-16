from abc import ABC
from typing import TYPE_CHECKING

from aiohttp import ClientSession

from .types import JsonDict

if TYPE_CHECKING:
    from .client import DockerClient


class SystemAPIBase(ABC):
    """
    Base Class for System API versions.
    """
    def __init__(self, client: 'DockerClient') -> None:
        self._client = client


class SystemAPI(SystemAPIBase):
    """
    System API.
    Docker Core API 1.25 compatible.
    """
    def __init__(self, client: 'DockerClient') -> None:
        super().__init__(client)
        self._baseuri = "http://1.25"

    async def version(self) -> JsonDict:
        async with ClientSession(connector=self._client.conn) as session:
            async with session.get("%s/version" % (self._baseuri)) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    raise Exception(await resp.json())
