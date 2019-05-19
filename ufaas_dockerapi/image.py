from abc import ABC
from typing import Optional, TYPE_CHECKING

from ufaas_dockerapi.types import DockerJSONResponse
from ufaas_dockerapi.utils import (api_delete, api_post, convert_bool,
                                   strip_nulls)

if TYPE_CHECKING:
    from ufaas_dockerapi.client import DockerClient


class ImageAPIBase(ABC):
    """
    Base Class for Image API versions.
    """
    def __init__(self, client: 'DockerClient') -> None:
        self._client = client


class ImageAPI(ImageAPIBase):
    """
    Image API.
    Docker Core API 1.25 compatible.
    """
    def __init__(self, client: 'DockerClient') -> None:
        super().__init__(client)
        self._baseuri = "http://1.25/images"

    async def pull(self, img_name: str, repo_uri: Optional[str] = None,
                   tag: Optional[str] = None,
                   platform: str = "") -> DockerJSONResponse:
        """
        Create an image by pulling it from a registry.
        Calls `https://docs.docker.com/engine/api/v1.39/#operation/ImageCreate`
        but provides a simple API for the most common use-case which is simply
        pulling from a Docker repository.
        """
        d = strip_nulls({"fromImage": img_name, "fromSrc": repo_uri,
                         "tag": tag, "platform": platform})

        return await api_post(self._client,
                              "%s/create" % self._baseuri, params=d,
                              streaming=True)

    async def import_source(self, image_uri: str, repo_identifier: str,
                            tag: Optional[str] = None,
                            platform: str = "") -> DockerJSONResponse:
        """
        Create an image by pulling it from a URI or from a file.
        Calls `https://docs.docker.com/engine/api/v1.39/#operation/ImageCreate`
        but provides a simple API for the most common use-case which is simply
        pulling from a Docker repository.
        TODO: Create method to create image given a file.
        """
        if image_uri != "-":
            raise Exception("Supplying image as request body not supported by \
                import_source().")

        d = strip_nulls({"repo_identifier": repo_identifier,
                         "fromSrc": image_uri, "tag": tag,
                         "platform": platform})

        return await api_post(self._client,
                              "%s/create" % self._baseuri, params=d,
                              streaming=True)

    async def remove(self, image: str, force: bool = False,
                     noprune: bool = False) -> DockerJSONResponse:
        """
        Remove an image, along with any untagged parent images that were
        referenced by that image.
        `image` can be the image name or the docker image ID.
        Calls `https://docs.docker.com/engine/api/v1.39/#operation/ImageDelete`
        """
        d = convert_bool({"force": force, "noprune": noprune})

        return await api_delete(self._client,
                                "%s/%s" % (self._baseuri, image),
                                params=d, streaming=True)
