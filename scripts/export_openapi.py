"""Write openapi.json from the FastAPI app. The spec is generated from code, so it cannot drift."""
import json
from pathlib import Path

from chess_api.server import app

Path('openapi.json').write_text(json.dumps(app.openapi(), indent=2) + '\n')
print('wrote openapi.json')
