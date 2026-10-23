from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.board import Board
from ...models.move import Move
from ...models.move_error import MoveError
from typing import cast



def _get_kwargs(
    id: str,
    *,
    body: Move,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/games/{id}/moves".format(id=quote(str(id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Board | MoveError | None:
    if response.status_code == 200:
        response_200 = Board.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = MoveError.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = MoveError.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = MoveError.from_dict(response.json())



        return response_404

    if response.status_code == 409:
        response_409 = MoveError.from_dict(response.json())



        return response_409

    if response.status_code == 422:
        response_422 = MoveError.from_dict(response.json())



        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Board | MoveError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    body: Move,

) -> Response[Board | MoveError]:
    """ Play one move

     Play one move in SAN, for example "e4" or "O-O". Illegal moves return 422 with a code that says why.

    Args:
        id (str):
        body (Move):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Board | MoveError]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: str,
    *,
    client: AuthenticatedClient,
    body: Move,

) -> Board | MoveError | None:
    """ Play one move

     Play one move in SAN, for example "e4" or "O-O". Illegal moves return 422 with a code that says why.

    Args:
        id (str):
        body (Move):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Board | MoveError
     """


    return sync_detailed(
        id=id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    body: Move,

) -> Response[Board | MoveError]:
    """ Play one move

     Play one move in SAN, for example "e4" or "O-O". Illegal moves return 422 with a code that says why.

    Args:
        id (str):
        body (Move):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Board | MoveError]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    body: Move,

) -> Board | MoveError | None:
    """ Play one move

     Play one move in SAN, for example "e4" or "O-O". Illegal moves return 422 with a code that says why.

    Args:
        id (str):
        body (Move):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Board | MoveError
     """


    return (await asyncio_detailed(
        id=id,
client=client,
body=body,

    )).parsed
