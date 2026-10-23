"""Replay the scenes from the talk against all three interfaces: HTTP, generated SDK and MCP."""
import httpx2
import pytest
from fastapi.testclient import TestClient
from fastmcp import Client

from agent_ready_chess_api_client import AuthenticatedClient
from agent_ready_chess_api_client.api.games import create_game, get_board, make_move
from agent_ready_chess_api_client.models import Move, MoveError, MoveErrorCode
from chess_api.server import app
from mcp_server.server import build

OPENING = ['e4', 'Nf6', 'Nf3', 'Ng4', 'Bc4', 'Ne3']  # slides 2-3
REST = ['Nc6', 'O-O', 'b6', 'Nc3', 'Bb7', 'Nh4', 'h6', 'Qh5', 'a5', 'Qxf7#']  # after dxe3, slides 5-12

http = TestClient(app)
PLAYER = {'Authorization': 'Bearer player-token'}


def new_game(moves=()):
    gid = http.post('/games', headers=PLAYER).json()['id']
    for m in moves:
        assert http.post(f'/games/{gid}/moves', json={'move': m}, headers=PLAYER).status_code == 200, m
    return gid


def sdk_client():
    # The SDK talks to the in-process app through the TestClient transport.
    c = AuthenticatedClient(base_url='http://testserver', token='player-token')
    c.set_httpx_client(TestClient(app, headers={'Authorization': 'Bearer player-token'}))
    return c


# ---------- HTTP: slides 3, 4, 10, 12 ----------
def test_slide3_castle_rejected_with_reason():
    gid = new_game(OPENING)
    r = http.post(f'/games/{gid}/moves', json={'move': 'O-O'}, headers=PLAYER)
    assert r.status_code == 422
    assert r.json()['code'] == 'CASTLING_THROUGH_CHECK'
    assert r.json()['detail'] == 'f1 is attacked by Ne3'


def test_slide4_reset_forbidden_for_player():
    gid = new_game()
    r = http.post(f'/games/{gid}/reset', headers=PLAYER)
    assert (r.status_code, r.json()['code']) == (403, 'FORBIDDEN')


def test_slide10_recover_then_castle():
    gid = new_game(OPENING)
    assert http.post(f'/games/{gid}/moves', json={'move': 'O-O'}, headers=PLAYER).status_code == 422
    r = http.post(f'/games/{gid}/moves', json={'move': 'dxe3'}, headers=PLAYER)
    assert (r.status_code, r.json()['next_turn']) == (200, 'black')


def test_slide12_full_game_ends_in_checkmate():
    gid = new_game(OPENING + ['dxe3'] + REST)
    assert http.get(f'/games/{gid}', headers=PLAYER).json()['status'] == 'checkmate'


def test_spec_declares_the_error_model():
    spec = app.openapi()
    move_422 = spec['paths']['/games/{id}/moves']['post']['responses']['422']
    assert move_422['content']['application/json']['schema']['$ref'].endswith('/MoveError')
    assert 'CASTLING_THROUGH_CHECK' in spec['components']['schemas']['MoveError']['properties']['code']['enum']


# ---------- SDK: slide 7 ----------
def test_sdk_returns_typed_error():
    c = sdk_client()
    gid = create_game.sync(client=c).id
    for m in OPENING:
        make_move.sync(gid, client=c, body=Move(move=m))
    res = make_move.sync(gid, client=c, body=Move(move='O-O'))
    assert isinstance(res, MoveError)
    assert res.code == MoveErrorCode.CASTLING_THROUGH_CHECK
    assert res.detail == 'f1 is attacked by Ne3'
    assert get_board.sync(gid, client=c).next_turn == 'white'


# ---------- MCP: slide 8 ----------
@pytest.fixture
def mcp():
    transport = httpx2.ASGITransport(app=app)
    return build(httpx2.AsyncClient(transport=transport, base_url='http://testserver',
                                    headers={'Authorization': 'Bearer player-token'}))


async def test_mcp_exposes_only_agent_tools(mcp):
    async with Client(mcp) as c:
        names = sorted(t.name for t in await c.list_tools())
    assert names == ['get_board', 'make_move']


async def test_mcp_agent_recovers_from_castling_error(mcp):
    gid = new_game(OPENING)
    async with Client(mcp) as c:
        bad = await c.call_tool('make_move', {'id': gid, 'move': 'O-O'}, raise_on_error=False)
        assert bad.is_error and 'CASTLING_THROUGH_CHECK' in bad.content[0].text
        ok = await c.call_tool('make_move', {'id': gid, 'move': 'dxe3'})
        assert ok.structured_content['next_turn'] == 'black'
