from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ufaas_dockerapi.types import DockerJSON


class DockerAPIException(Exception):
    """
    payload contains the HTTP Status Code and the JSON error message.
    """
    def __init__(self, http_status: int, json_message: 'DockerJSON'):
        self.http_status = http_status
        self.json_message = json_message
