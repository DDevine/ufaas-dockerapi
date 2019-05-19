from abc import ABC
from dataclasses import asdict
from typing import Optional, TYPE_CHECKING

from ufaas_dockerapi.config import ContainerConfig, config_dict_factory
from ufaas_dockerapi.types import DockerJSONResponse
from ufaas_dockerapi.utils import (api_delete, api_post, convert_bool,
                                   strip_nulls)

if TYPE_CHECKING:
    from ufaas_dockerapi.client import DockerClient


class ContainerAPIBase(ABC):
    """
    Base Class for Container API versions.
    """
    def __init__(self, client: 'DockerClient') -> None:
        self._client = client


class ContainerAPI(ContainerAPIBase):
    """
    Container API.
    Docker Core API 1.25 compatible.
    """
    def __init__(self, client: 'DockerClient') -> None:
        super().__init__(client)
        self._baseuri = "http://1.25/containers"

    async def create(self, container_name: str,
                     config: ContainerConfig) -> DockerJSONResponse:
        """
        Create a Docker container given a name and ContainerConfig object.

        `https://docs.docker.com/engine/api/v1.39/#operation/ContainerCreate`
        """
        d = {"name": container_name}

        container_config = strip_nulls(asdict(config,
                                       dict_factory=config_dict_factory))

        return await api_post(self._client,
                              "%s/create" % self._baseuri, params=d,
                              json_body=container_config, streaming=False)

    async def delete(self, container: str, force_stop: Optional[bool] = None,
                     remove_volumes: Optional[bool] = None,
                     remove_link: Optional[bool] = None  # NOTE: not in 1.25
                     ) -> DockerJSONResponse:
        """
        Delete a container.

        `https://docs.docker.com/engine/api/v1.39/#operation/ContainerDelete`
        """
        d = {"v": remove_volumes, "force": force_stop, "link": remove_link}
        d = convert_bool(strip_nulls(d))

        return await api_delete(self._client,
                                "%s/%s" % (self._baseuri, container), params=d,
                                streaming=True)
