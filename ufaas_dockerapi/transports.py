from abc import ABC

from aiohttp import BaseConnector, UnixConnector


class TransportBase(ABC):
    """
    Base Class for Container API versions.
    """


class DockerSock(TransportBase):
    """
    Docker Unix Socket transport.
    """
    def __init__(self, path: str = "/var/run/docker.sock") -> None:
        self._socket_path = path

    def create_connection(self) -> BaseConnector:
        return UnixConnector(path=self._socket_path)
