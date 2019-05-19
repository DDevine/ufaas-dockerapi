from abc import ABC
from typing import TYPE_CHECKING

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
