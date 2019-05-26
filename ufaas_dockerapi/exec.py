from abc import ABC
from dataclasses import asdict
from typing import TYPE_CHECKING

from ufaas_dockerapi.config import ExecConfig, config_dict_factory
from ufaas_dockerapi.types import DockerJSONResponse
from ufaas_dockerapi.utils import (api_post, strip_nulls)

if TYPE_CHECKING:
    from ufaas_dockerapi.client import DockerClient


class ExecAPIBase(ABC):
    """
    Base Class for Exec API versions.
    """
    def __init__(self, client: 'DockerClient') -> None:
        self._client = client


class ExecAPI(ExecAPIBase):
    """
    Exec API.
    Docker Core API 1.25 compatible.
    """
    def __init__(self, client: 'DockerClient') -> None:
        super().__init__(client)
        self._baseuri = "http://1.25"

    async def run(self, container_name: str,
                  config: ExecConfig, detach: bool = False,
                  tty: bool = True) -> DockerJSONResponse:
        """
        Performs a "docker exec". Note this only works with running containers.
        """
        _, res = await self.exec_create(container_name, config)
        exec_id = res["Id"]  # type: ignore
        return await self.exec_start(exec_id, detach=detach, tty=tty)

    async def exec_create(self, container_name: str,
                          config: ExecConfig) -> DockerJSONResponse:
        """
        Run a command in an already running container.
        Sets up an Exec instance. This needs to be used with `exec_start` to
        run.

        `https://docs.docker.com/engine/api/v1.39/#operation/ContainerExec`
        """
        exec_config = strip_nulls(asdict(config,
                                         dict_factory=config_dict_factory))
        uri = "%s/containers/%s/exec" % (self._baseuri, container_name)
        return await api_post(self._client,
                              uri,
                              json_body=exec_config, streaming=False)

    async def exec_start(self, exec_id: str, detach: bool = False,
                         tty: bool = True) -> DockerJSONResponse:
        """
        Starts are previously setup exec instance (eg. with `exec_create`).
        `https://docs.docker.com/engine/api/v1.39/#operation/ExecStart`
        """
        opts = {"detach": detach, "tty": tty}

        return await api_post(self._client,
                              "%s/exec/%s/start" % (self._baseuri, exec_id),
                              json_body=opts, streaming=True)
