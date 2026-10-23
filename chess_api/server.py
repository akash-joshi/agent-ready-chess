"""Chess API: the single source of truth. The OpenAPI spec, the SDK, the MCP server and the docs are generated from it."""
from typing import Annotated, Any, Literal

import chess
from fastapi import Depends, FastAPI
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(
    title='Agent-ready chess API',
    version='1.0.0',
    description='A small chess API used to show how one contract feeds an SDK, an MCP server and docs.',
)

# ---------- contract ----------
ErrorCode = Literal[
    'CASTLING_THROUGH_CHECK', 'ILLEGAL_MOVE', 'NOT_YOUR_TURN', 'STALE_BOARD', 'GAME_NOT_FOUND', 'FORBIDDEN', 'UNAUTHORIZED',
]


class Move(BaseModel):
    move: str = Field(description='Move in SAN, for example "e4", "Nf3" or "O-O".', examples=['O-O'])
    board_version: int | None = Field(None, description='Version you last read. If it is out of date, the move is rejected with STALE_BOARD.')


class Board(BaseModel):
    id: str
    fen: str = Field(description='Board position in FEN.')
    board_version: int
    next_turn: Literal['white', 'black']
    status: Literal['in_progress', 'checkmate', 'stalemate', 'draw']
    legal_moves: list[str] = Field(description='Legal moves for the side to move, in SAN.')


class MoveError(BaseModel):
    code: ErrorCode = Field(description='Stable, machine-readable error code. Branch on this, not on detail.')
    detail: str = Field(description='Human-readable explanation of why the request failed.')
    hint: str | None = Field(None, description='What to do next.')


ERRORS: dict[int | str, dict[str, Any]] = {r: {'model': MoveError} for r in (401, 403, 404, 409, 422)}

# ---------- state ----------
TOKENS = {'player-token': 'player', 'viewer-token': 'viewer', 'admin-token': 'admin'}
GAMES: dict[str, chess.Board] = {}
VERSIONS: dict[str, int] = {}


class ApiError(Exception):
    def __init__(self, status: int, code: ErrorCode, detail: str, hint: str | None = None):
        self.status, self.body = status, MoveError(code=code, detail=detail, hint=hint)


@app.exception_handler(ApiError)
async def api_error(_, exc: ApiError):
    return JSONResponse(exc.body.model_dump(exclude_none=True), status_code=exc.status)


bearer = HTTPBearer(auto_error=False, description='Demo tokens: player-token, viewer-token, admin-token')


def role(creds: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)] = None) -> str:
    token = creds.credentials if creds else ''
    if token not in TOKENS:
        raise ApiError(401, 'UNAUTHORIZED', 'Missing or unknown bearer token.')
    return TOKENS[token]


def game(id: str) -> chess.Board:
    if id not in GAMES:
        raise ApiError(404, 'GAME_NOT_FOUND', f'No game with id {id!r}.', 'Create a game with POST /games.')
    return GAMES[id]


def view(id: str) -> Board:
    b = GAMES[id]
    status = 'checkmate' if b.is_checkmate() else 'stalemate' if b.is_stalemate() else 'draw' if b.is_game_over() else 'in_progress'
    return Board(id=id, fen=b.fen(), board_version=VERSIONS[id], next_turn='white' if b.turn else 'black',
                 status=status, legal_moves=sorted(b.san(m) for m in b.legal_moves))


def castling_through_check(b: chess.Board, san: str) -> str | None:
    """Explain why O-O / O-O-O is illegal when the only problem is an attacked square."""
    side = {'O-O': (chess.F1, chess.G1, 'kingside'), 'O-O-O': (chess.D1, chess.C1, 'queenside')}.get(san.replace('0', 'O'))
    if not side:
        return None
    rank = 0 if b.turn else 7
    squares = [chess.square(chess.square_file(s), rank) for s in side[:2]]
    rights = b.has_kingside_castling_rights(b.turn) if side[2] == 'kingside' else b.has_queenside_castling_rights(b.turn)
    if not rights or any(b.piece_at(s) for s in squares) or b.is_check():
        return None
    for s in squares:
        attackers = b.attackers(not b.turn, s)
        if attackers:
            a = attackers.pop()
            piece = b.piece_at(a).symbol().upper().replace('P', '')
            return f'{chess.square_name(s)} is attacked by {piece}{chess.square_name(a)}'
    return None


# ---------- operations ----------
@app.post('/games', response_model=Board, status_code=201, operation_id='create_game', tags=['games'],
          summary='Start a new game', responses=ERRORS)
def create_game(r: str = Depends(role)) -> Board:
    id = str(len(GAMES) + 42)
    GAMES[id], VERSIONS[id] = chess.Board(), 0
    return view(id)


@app.get('/games/{id}', response_model=Board, operation_id='get_board', tags=['games'],
         summary='Read the current board', description='Returns the position, whose turn it is and every legal move.',
         responses=ERRORS)
def get_board(id: str, r: str = Depends(role)) -> Board:
    game(id)
    return view(id)


@app.post('/games/{id}/moves', response_model=Board, operation_id='make_move', tags=['games'],
          summary='Play one move', description='Play one move in SAN, for example "e4" or "O-O". '
          'Illegal moves return 422 with a code that says why.', responses=ERRORS)
def make_move(id: str, body: Move, r: str = Depends(role)) -> Board:
    b = game(id)
    if r == 'viewer':
        raise ApiError(403, 'FORBIDDEN', 'Viewers can read the board but cannot move.')
    if body.board_version is not None and body.board_version != VERSIONS[id]:
        raise ApiError(409, 'STALE_BOARD', f'Board is at version {VERSIONS[id]}, not {body.board_version}.', 'Read the board again, then retry.')
    reason = castling_through_check(b, body.move)
    if reason:
        raise ApiError(422, 'CASTLING_THROUGH_CHECK', reason, 'Move or capture the attacking piece, then castle.')
    try:
        b.push_san(body.move)
    except ValueError:
        raise ApiError(422, 'ILLEGAL_MOVE', f'{body.move!r} is not legal here.', 'Pick one of legal_moves from get_board.')
    VERSIONS[id] += 1
    return view(id)


@app.post('/games/{id}/reset', response_model=Board, operation_id='reset_game', tags=['admin'],
          summary='Reset a game to the start position (admin only)', responses=ERRORS)
def reset_game(id: str, r: str = Depends(role)) -> Board:
    game(id)
    if r != 'admin':
        raise ApiError(403, 'FORBIDDEN', f'Role {r!r} may not reset games.')
    GAMES[id], VERSIONS[id] = chess.Board(), VERSIONS[id] + 1
    return view(id)
