# flake8: noqa
from typing import Any, Dict, List, Union

JsonDict = Dict[str, Any]  # Apparently this is what Guido uses...

# Docker sometimes returns streamed JSON.
DockerJSONResponse = Union[List[JsonDict], JsonDict]

from .container import ContainerAPIBase
from .exec import ExecAPIBase
from .image import ImageAPIBase
from .system import SystemAPIBase
from .transports import DockerSock


TransportType = Union[DockerSock]

ContainerAPIType = ContainerAPIBase
ImageAPIType = ImageAPIBase
ExecAPIType = ExecAPIBase
SystemAPIType = SystemAPIBase
