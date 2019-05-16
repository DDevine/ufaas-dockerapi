from abc import ABC
from typing import Any


class ContainerAPIBase(ABC):
    """
    Base Class for Container API versions.
    """
    def __init__(self, client: Any) -> None:  # client is Any, circular import.
        self._client = client


class ContainerAPI(ContainerAPIBase):
    """
    Container API.
    Docker Core API 1.25 compatible.
    """
