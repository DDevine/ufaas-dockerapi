import json
from typing import List, Optional, TYPE_CHECKING

from aiohttp import ClientSession, ClientWebSocketResponse

from ufaas_dockerapi.exceptions import DockerAPIException
from ufaas_dockerapi.types import DockerJSONResponse, JsonDict

if TYPE_CHECKING:
    from ufaas_dockerapi.client import DockerClient


async def api_call(client: 'DockerClient', method: str, uri: str,
                   params: Optional[JsonDict] = None,
                   json_body: Optional[JsonDict] = None,
                   streaming: bool = False) -> DockerJSONResponse:
    """
    Helper method to perform a HTTP requests and handle responses from the
    Docker API.
    """
    async with ClientSession(connector=client.conn) as session:
        if method.upper() == "GET":
            sess = session.get(uri, params=params, json=json_body)
        elif method.upper() == "PUT":
            sess = session.put(uri, params=params, json=json_body)
        elif method.upper() == "POST":
            sess = session.post(uri, params=params, json=json_body)
        elif method.upper() == "DELETE":
            sess = session.delete(uri, params=params, json=json_body)
        else:
            raise Exception("Unknown HTTP verb: %s" % method)
        async with sess as resp:
            if resp.status in (200, 201, 204):
                if streaming:
                    statuses: List[str] = (await resp.text()).split("\r\n")
                    return (resp.status, [json.loads(i)
                            for i in statuses if i != ""])
                else:
                    if 'CONTENT-TYPE' in resp.headers:
                        return (resp.status, await resp.json())
                    else:
                        return (resp.status, "")

            else:
                raise DockerAPIException(resp.status, await resp.json())


async def api_get(client: 'DockerClient', uri: str,
                  params: Optional[JsonDict] = None,
                  json_body: Optional[JsonDict] = None,
                  streaming: bool = False) -> DockerJSONResponse:
    """
    Helper method to perform a GET and handle responses from the Docker API.
    """
    return await api_call(client, "GET", uri, params=params,
                          json_body=json_body, streaming=streaming)


async def api_post(client: 'DockerClient', uri: str,
                   params: Optional[JsonDict] = None,
                   json_body: Optional[JsonDict] = None,
                   streaming: bool = False) -> DockerJSONResponse:
    """
    Helper method to perform a POST and handle responses from the Docker API.
    """
    return await api_call(client, "POST", uri, params=params,
                          json_body=json_body, streaming=streaming)


async def api_delete(client: 'DockerClient', uri: str,
                     params: Optional[JsonDict] = None,
                     json_body: Optional[JsonDict] = None,
                     streaming: bool = False) -> DockerJSONResponse:
    """
    Helper method to perform a DELETE and handle responses from the Docker API.
    """
    return await api_call(client, "DELETE", uri, params=params,
                          json_body=json_body, streaming=streaming)


async def get_websocket(client: 'DockerClient',
                        uri: str) -> ClientWebSocketResponse:
    """
    Returns a AIOHttp WebSocket object.
    If you want query params you must build them and add them to the URI.
    """
    async with ClientSession(connector=client.conn) as session:
        return await session.ws_connect(uri)


def convert_bool(d: JsonDict) -> JsonDict:
    """
    Booleans need to be converted to JS friendly strings in URL parameters.
    """
    out = dict({})
    for k, v in d.items():
        if type(v) == bool:
            if v:
                out[k] = "true"
            else:
                out[k] = "false"
        else:
            out[k] = v
    return out


def strip_nulls(d: JsonDict) -> JsonDict:
    """
    Remove items that have the value `None` from the dictionary so that they
    are not needlessly added to the URI parameters.
    """
    return {k: v for k, v in d.items() if v is not None}
