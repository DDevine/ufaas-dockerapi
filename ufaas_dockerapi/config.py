"""
This module of config objects should be backwards compatible to Docker Engine
API 1.25.
If future APIs are not backwards compatible in terms of config objects, then
the user of this library will instead import a different module of config files
or other config objects.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from ufaas_dockerapi.types import JsonDict # noqa: #F401

# NOTE: Configs are dataclasses because of their ability to recursively convert
# to dictionaries that are easily JSON serialisable. However, to get a nice API
# with Python friendly key names a mapping function is needed for
# `dataclass.asdict` that must convert key names to what Docker expects.
# Most keys will automaticallly be converted but the keys below are exceptions.
# See `config.config_dict_factory` for further explanation.
DOCKER_KEYMAP = {
    "host_name": 'Hostname',
    "domain_name": 'Domainname',
    "entry_point": 'Entrypoint',
    "network_config": 'NetworkingConfig'
}


@dataclass
class ConfigBase:
    """
    The base class for Docker config objects for typing reasons.
    """


@dataclass
class AuthConfig(ConfigBase):
    # TODO: Implement auth handling. This class is just a placeholder.
    username: str
    password: str


@dataclass
class ExposedPortsConfig(ConfigBase):
    """
    An object mapping ports to an empty object in the form:
    {"<port>/<tcp|udp|sctp>": {}}
    """


@dataclass
class HealthCheckConfig(ConfigBase):
    """
    Configure the Docker health checking.
    """
    # TODO: implement.


@dataclass
class HostConfig(ConfigBase):
    """
    Container configuration for a specific host.
    """
    # TODO: implement


@dataclass
class IPAMConfig(ConfigBase):
    """
    Network configuration for an endpoint.
    """
    network_id: str
    endpoint_id: str
    gateway_addr: str
    ip4_addr: str
    ip4_prefix: int
    ip6_gateway: str
    global_ip6_addr: str
    global_ip6_prefix: int  # This should be 64bit
    mac_address: str
    links: List[str]
    aliases: List[str]
    driver_opts: Optional['JsonDict'] = None


@dataclass
class NetworkConfig(ConfigBase):
    """
    A container's networking configuration.
    """
    endpoints_config: Dict[str, IPAMConfig]


@dataclass()
class ContainerConfig(ConfigBase):
    """
    A class that represents the configuration for a Docker container.
    Based off
    `https://docs.docker.com/engine/api/v1.39/#operation/ContainerCreate`

    Most fields are optional.
    """
    image: str
    hostname: Optional[str] = None
    domain_name: Optional[str] = None
    container_user: Optional[str] = None
    attach_stdin: Optional[bool] = None  # Default: False
    attach_stdout: Optional[bool] = None  # Default: True
    attach_stderr: Optional[bool] = None  # Default: True
    exposed_ports: Optional[ExposedPortsConfig] = None
    tty: Optional[bool] = None  # Default False
    open_stdin: Optional[bool] = None  # Default: False
    stdin_once: Optional[bool] = None  # Default: False
    env: Dict[str, Union[str, int, float]] = field(default_factory=dict)
    cmd: List[str] = field(default_factory=list)
    health_check: Optional[HealthCheckConfig] = None
    volumes: Optional[Dict[Any, Any]] = None
    working_dir: Optional[str] = None
    entry_point: List[str] = field(default_factory=list)
    network_disabled: Optional[bool] = None  # Default: False
    mac_address: Optional[str] = None
    on_build: Optional[List[str]] = None
    labels: Optional['JsonDict'] = None
    stop_signal: Optional[str] = None  # Default: "SIGTERM"
    stop_timeout: Optional[int] = None  # Default: 10
    shell: Optional[List[str]] = None
    host_config: Optional[HostConfig] = None
    network_config: Optional[NetworkConfig] = None


@dataclass
class ExecConfig(ConfigBase):
    """
    A class that represents Exec configuration. Similar, but different to
    ContainerConfig.

    `https://docs.docker.com/engine/api/v1.39/#operation/ContainerExec`
    """
    attach_stdin: Optional[bool] = None  # Default: False
    attach_stdout: Optional[bool] = None  # Default: True
    attach_stderr: Optional[bool] = None  # Default: True
    detach_keysequence: Optional[str] = None  # Default: "ctrl-p,ctrl-q"
    tty: Optional[bool] = None  # Default: False
    env: Dict[str, Union[str, int, float]] = field(default_factory=dict)
    cmd: List[str] = field(default_factory=list)
    extended_privileges: Optional[bool] = None  # Default: False
    container_user: Optional[str] = None
    working_dir: Optional[str] = None


def config_dict_factory(cfg: Any) -> 'JsonDict':
    """
    Rename the key names of the given mapping `cfg` to a new dictionary with
    Docker JSON API compatible key names. This factory will be applied
    recursively on nested dataclasses.

    All Docker config object fields have their first letter capitalised and use
    Camel Case. We don't have to map single-word fields if the word is the same
    or fields that are correct other than case and use of underscores.
    This means the config.DOCKER_KEYMAP is surprisingly small. It is important
    to note that key mappings across Config classes must not collide.
    eg. Do not have A.foo --> "Foo" and B.foo --> "FOO".

    Some fields have their value format converted here too, such as `env` which
    is converted from a python-friendly dictionary to an array of strings.
    """
    out = dict({})
    for key, val in cfg:
        anyval: Any = None  # Deal with type conversions.
        if key == "env":
            # Build list of 'KEY=VAL'-like strings suitable for unix
            # environment variables.
            anyval = ["%s=%s" % (k, v) for k, v in val.items()]
        else:
            anyval = val
        try:
            out[DOCKER_KEYMAP[key]] = anyval
        except KeyError:
            # Attempt to automatically translate the key name.
            out[" ".join(key.split("_")).title().strip(" ")] = anyval
    return out
