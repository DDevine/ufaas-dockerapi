from __future__ import annotations  # Makes all type annotations strings, fixes
# circular import issue with type checking.

from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import DockerClient


class ImageAPIBase(ABC):
    """
    Base Class for Image API versions.
    """
    def __init__(self, client: DockerClient) -> None:
        self._client = client


class ImageAPI(ImageAPIBase):
    """
    Image API.
    Docker Core API 1.25 compatible.
    """
