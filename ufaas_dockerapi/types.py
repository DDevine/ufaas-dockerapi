# flake8: noqa
from typing import Any, Dict, Union

JsonDict = Dict[str, Any]  # Apparently this is what Guido uses...

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
