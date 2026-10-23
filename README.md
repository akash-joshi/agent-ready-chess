# Agent-ready chess

Code sample for the talk **Your API Is Not Agent-Ready Yet** (Birmingham Tech Week 2026).

One API contract feeds three interfaces: a typed SDK, an MCP server for agents, and docs. The chess game from the slides runs against all of them in the tests.

```
chess_api/server.py  ->  openapi.json  ->  sdk/            (openapi-python-client)
                                       ->  mcp_server/     (FastMCP.from_openapi)
                                       ->  /docs           (Swagger UI, built into FastAPI)
```

## Run it

```sh
uv sync
./scripts/generate.sh        # openapi.json + sdk/ from the server code
uv run pytest                # replays the scenes from the slides
uv run uvicorn chess_api.server:app   # API on :8000, docs on :8000/docs
uv run python -m mcp_server.server    # MCP server over stdio, talks to the API on :8000
```

Demo tokens: `player-token`, `viewer-token`, `admin-token`.

## Slide to file

| Slide | What it shows | Where |
|---|---|---|
| 3. The integration problem | Castling is rejected | `tests/test_slides.py::test_slide3_castle_rejected_with_reason` |
| 4. Authentication and access control | A player may not reset the game: `403 FORBIDDEN` | `chess_api/server.py` `reset_game`, `test_slide4_...` |
| 5. One shared contract | `POST /games/{id}/moves`, `422 CASTLING_THROUGH_CHECK` | `chess_api/server.py` `Move`, `Board`, `MoveError` |
| 6. OpenAPI | The spec is generated from the code | `scripts/export_openapi.py`, `openapi.json` |
| 7. SDK | The castle error comes back as a typed `MoveError` | `sdk/`, `test_sdk_returns_typed_error` |
| 8. MCP | The agent sees `get_board` and `make_move` only. No reset tool | `mcp_server/server.py`, `test_mcp_exposes_only_agent_tools` |
| 9. Docs | Error codes come with a hint for what to do next | `MoveError.hint`, `/docs` |
| 10. Worked example | The agent reads the error, plays dxe3 | `test_mcp_agent_recovers_from_castling_error` |
| 12. Checkmate | The full game ends in mate | `test_slide12_full_game_ends_in_checkmate` |

## The game

1.e4 Nf6 2.Nf3 Ng4 3.Bc4 Ne3 (O-O rejected: f1 is attacked by Ne3) 4.dxe3 Nc6 5.O-O b6 6.Nc3 Bb7 7.Nh4 h6 8.Qh5 a5 9.Qxf7#
