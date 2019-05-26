# flake8: noqa
from typing import Any, Dict, List, Tuple, Union

JsonDict = Dict[str, Any]

DockerJSON = Union[List[JsonDict], JsonDict]
# Docker sometimes returns streamed JSON. We also want the HTTP code as int.
DockerJSONResponse = Tuple[int, DockerJSON]

from ufaas_dockerapi.config import ConfigBase
from ufaas_dockerapi.container import ContainerAPIBase
from ufaas_dockerapi.exec import ExecAPIBase
from ufaas_dockerapi.image import ImageAPIBase
from ufaas_dockerapi.system import SystemAPIBase
from ufaas_dockerapi.transports import DockerSock

TransportType = Union[DockerSock]

ContainerAPIType = ContainerAPIBase
ImageAPIType = ImageAPIBase
ExecAPIType = ExecAPIBase
SystemAPIType = SystemAPIBase
ConfigType = ConfigBase