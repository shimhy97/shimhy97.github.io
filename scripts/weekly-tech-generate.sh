#!/usr/bin/env bash
# 주간 다이제스트 Python 의존성을 프로젝트 로컬 venv에 맞춘 뒤 생성 스크립트를 실행한다.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_DIR="$PROJECT_ROOT/.venv"

if [[ ! -d "$VENV_DIR" ]]; then
  python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r "$PROJECT_ROOT/scripts/weekly-tech/requirements.txt"
python "$PROJECT_ROOT/scripts/weekly-tech/generate_digest.py" "$@"
