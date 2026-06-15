#!/bin/zsh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV_DIR="$ROOT_DIR/.venv"

python3 -m venv "$VENV_DIR" --system-site-packages
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip
python -m pip install -e "$ROOT_DIR"

echo "Base environment ready at $VENV_DIR"
echo "Optional plotting support: python -m pip install '$ROOT_DIR[plot]'"
