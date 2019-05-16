from typing import Optional, TYPE_CHECKING, Tuple

from .config import AuthConfig
from .transports import DockerSock
from .types import (ContainerAPIType, ExecAPIType, ImageAPIType, SystemAPIType,
                    TransportType)

if TYPE_CHECKING:
    from aiohttp import BaseConnector


class DockerClient:
    def __init__(self, transport: TransportType,
                 auth: Optional[AuthConfig] = None,
                 version: Tuple[int, int] = (1, 25)):
        self._version = version
        self._transport = transport

        if version >= (1, 25):
            from .container import ContainerAPI
            from .image import ImageAPI
            from .exec import ExecAPI
            from .system import SystemAPI
            self._container = ContainerAPI(self)
            self._image = ImageAPI(self)
            self._exec = ExecAPI(self)
            self._system = SystemAPI(self)

    @property
    def conn(self) -> 'BaseConnector':
        """
        Helper that returns the aiohttp connection object for the transport
        in use.
        """
        return self._transport._conn

    @property
    def container(self) -> ContainerAPIType:
        return self._container

    @property
    def image(self) -> ImageAPIType:
        return self._image

    @property
    def exec(self) -> ExecAPIType:
        return self._exec

    @property
    def system(self) -> SystemAPIType:
        return self._system


def default_transport() -> DockerSock:
    """
    Helper which returns a basic Unix transport which works for most systems.
    """
    return DockerSock()
