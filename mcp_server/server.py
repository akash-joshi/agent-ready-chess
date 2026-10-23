"""MCP server generated from openapi.json with FastMCP.

- Only the operations an agent needs become tools: get_board and make_move. reset_game and create_game are excluded.
- Generated descriptions are replaced with ones written for an agent.
"""
import json
import os
from pathlib import Path

import httpx2
from fastmcp import FastMCP
from fastmcp.server.providers.openapi import MCPType, RouteMap

SPEC = json.loads((Path(__file__).parent.parent / 'openapi.json').read_text())
BASE_URL = os.environ.get('CHESS_API_URL', 'http://127.0.0.1:8000')
TOKEN = os.environ.get('CHESS_API_TOKEN', 'player-token')

AGENT_TOOLS = {'get_board', 'make_move'}

DESCRIPTIONS = {
    'get_board': 'Read the current board: position (FEN), whose turn it is, and every legal move in SAN. '
                 'Call this before choosing a move.',
    'make_move': 'Play one move in SAN, for example "e4" or "O-O". On failure the result has a code: '
                 'CASTLING_THROUGH_CHECK means a square the king crosses is attacked - move or capture the attacker, then castle. '
                 'ILLEGAL_MOVE means pick one of legal_moves. STALE_BOARD means read the board again.',
}


def only_agent_tools(route, mcp_type):
    return mcp_type if route.operation_id in AGENT_TOOLS else MCPType.EXCLUDE


def rewrite(route, component):
    if route.operation_id in DESCRIPTIONS:
        component.description = DESCRIPTIONS[route.operation_id]


def build(client: httpx2.AsyncClient | None = None) -> FastMCP:
    client = client or httpx2.AsyncClient(base_url=BASE_URL, headers={'Authorization': f'Bearer {TOKEN}'})
    return FastMCP.from_openapi(
        openapi_spec=SPEC,
        client=client,
        name='chess',
        route_maps=[RouteMap(mcp_type=MCPType.TOOL)],
        route_map_fn=only_agent_tools,
        mcp_component_fn=rewrite,
    )


if __name__ == '__main__':
    build().run()
