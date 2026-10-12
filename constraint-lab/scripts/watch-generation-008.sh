#!/usr/bin/env bash
# Print Generation 008 status every five seconds.
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ -x .venv/bin/python ]]; then
  PY=.venv/bin/python
else
  PY=python3
fi
exec "$PY" -m rs_constraint_lab generation008 status --watch 5 "$@"
