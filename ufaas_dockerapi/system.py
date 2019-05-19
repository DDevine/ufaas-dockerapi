from abc import ABC
from typing import TYPE_CHECKING

from ufaas_dockerapi.types import DockerJSONResponse
from ufaas_dockerapi.utils import api_get

if TYPE_CHECKING:
    from ufaas_dockerapi.client import DockerClient


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

    async def version(self) -> DockerJSONResponse:
        """
        Retrieve Docker version information.
        """
        return await api_get(self._client, "%s/version" % self._baseuri)
