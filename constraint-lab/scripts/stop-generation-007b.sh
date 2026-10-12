#!/usr/bin/env bash
# Ask the Generation 007B supervisor to stop after the current batch.
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ -x .venv/bin/python ]]; then
  PY=.venv/bin/python
else
  PY=python3
fi
exec "$PY" -m rs_constraint_lab generation007b stop "$@"
