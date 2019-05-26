from abc import ABC
from dataclasses import asdict
from typing import Optional, TYPE_CHECKING

from aiohttp import ClientWebSocketResponse

from ufaas_dockerapi.config import ContainerConfig, config_dict_factory
from ufaas_dockerapi.types import DockerJSONResponse
from ufaas_dockerapi.utils import (api_delete, api_post, convert_bool,
                                   get_websocket, strip_nulls)

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
        self._baseuri = "http://v1.25/containers"

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

    async def start(self, container_name: str,
                    detach_keysequence: Optional[str] = None
                    ) -> DockerJSONResponse:
        """
        Start a Docker container.

        `https://docs.docker.com/engine/api/v1.39/#operation/ContainerStart`
        """
        d = strip_nulls({"detachKeys": detach_keysequence})
        return await api_post(self._client,
                              "%s/%s/start" % (self._baseuri, container_name),
                              params=d, streaming=False)

    async def stop(self, container_name: str,
                   timeout: Optional[int] = None) -> DockerJSONResponse:
        """
        Stop a Docker container.

        `https://docs.docker.com/engine/api/v1.39/#operation/ContainerStop`
        """
        d = strip_nulls({"t": timeout})
        return await api_post(self._client,
                              "%s/%s/stop" % (self._baseuri, container_name),
                              params=d, streaming=False)

    async def restart(self, container_name: str,
                      timeout: Optional[int] = None) -> DockerJSONResponse:
        """
        Restart a Docker container.

        `https://docs.docker.com/engine/api/v1.39/#operation/ContainerRestart`
        """
        d = strip_nulls({"t": timeout})
        uri = "%s/%s/restart" % (self._baseuri, container_name)
        return await api_post(self._client, uri, params=d, streaming=False)

    async def attach_websocket(self, container_name: str,
                               detach_keysequence: Optional[str] = None,
                               return_logs: Optional[bool] = None,
                               return_stream: Optional[bool] = None,
                               attach_stdin: Optional[bool] = None,
                               attach_stdout: Optional[bool] = None,
                               attach_stderr: Optional[bool] = None,
                               ) -> ClientWebSocketResponse:
        """
        Returns an AIOHTTP websocket attached to the container.
        """
        # AIOHTTP doesn't support query parameters as an argument to
        # ws_connect so we must build the URI with params ourselves.
        params = convert_bool(strip_nulls({
            "detachKeys": detach_keysequence,
            "logs": return_logs,
            "stdin": attach_stdin,
            "stdout": attach_stdout,
            "stderr": attach_stderr,
            "stream": return_stream
            }))

        if len(params.keys()) > 0:
            # Assemble query parameters into string.
            p = ["%s=%s" % (k, v) for k, v in params.items()]
            querystr = "?%s" % "&".join(p)
        else:
            querystr = ""

        uri = "%s/%s/attach/ws%s" % (self._baseuri, container_name, querystr)
        return await get_websocket(self._client, uri)


class Container:
    """
    Represents a created container. API methods can be called with this object
    providing a object-oriented interface.
    """

    def __init__(self, config: Optional[ContainerConfig] = None,
                 created: bool = True, running: bool = False):
        """
        A container object configured based on the `config` object given.
        `created` should be True if the container already exists in Docker.
        `running` should be True if the container is already running in Docker.
        """
        self._created = created
        self._running = running
        self._config = config

    async def create(self) -> None:
        """
        Create this container in Docker.
        """
        if not self._running and not self._created:
            # Go forward.
            pass
        else:
            # Should we raise exception here? Or no news is good news?
            return
