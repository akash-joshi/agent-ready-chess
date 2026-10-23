#!/usr/bin/env sh
# Regenerate the contract and the SDK from the server code.
set -e
cd "$(dirname "$0")/.."
PYTHONPATH=. uv run python scripts/export_openapi.py
rm -rf sdk
PATH="$PWD/.venv/bin:$PATH" uv run openapi-python-client generate --path openapi.json --output-path sdk
