#!/usr/bin/env bash
# Ralph loop wrapper for this repository.
# 공식 Ralph 흐름은 유지하되, 작업 상태 파일을 프로젝트 루트 기준으로 읽도록 조정한다.

set -euo pipefail

show_usage() {
  cat <<'EOF'
Usage: ./scripts/ralph/ralph.sh [--tool amp|claude] [max_iterations]

Examples:
  ./scripts/ralph/ralph.sh --tool claude 5
  ./scripts/ralph/ralph.sh 10
EOF
}

TOOL="claude"
MAX_ITERATIONS=10

while [[ $# -gt 0 ]]; do
  case "$1" in
    --tool)
      TOOL="${2:-}"
      shift 2
      ;;
    --tool=*)
      TOOL="${1#*=}"
      shift
      ;;
    -h|--help)
      show_usage
      exit 0
      ;;
    *)
      if [[ "$1" =~ ^[0-9]+$ ]]; then
        MAX_ITERATIONS="$1"
      else
        echo "Error: Unknown argument '$1'"
        show_usage
        exit 1
      fi
      shift
      ;;
  esac
done

if [[ "$TOOL" != "amp" && "$TOOL" != "claude" ]]; then
  echo "Error: Invalid tool '$TOOL'. Must be 'amp' or 'claude'."
  exit 1
fi

if ! [[ "$MAX_ITERATIONS" =~ ^[0-9]+$ ]]; then
  echo "Error: max_iterations must be a positive integer."
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PRD_FILE="$PROJECT_ROOT/prd.json"
PROGRESS_FILE="$PROJECT_ROOT/progress.txt"
ARCHIVE_DIR="$PROJECT_ROOT/archive"
LAST_BRANCH_FILE="$SCRIPT_DIR/.last-branch"
PROMPT_FILE="$SCRIPT_DIR/prompt.md"
CLAUDE_FILE="$SCRIPT_DIR/CLAUDE.md"

require_command() {
  local command_name="$1"

  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "Error: '$command_name' is required but not installed."
    exit 1
  fi
}

require_file() {
  local file_path="$1"

  if [[ ! -f "$file_path" ]]; then
    echo "Error: Required file not found: $file_path"
    exit 1
  fi
}

initialize_progress_file() {
  if [[ -f "$PROGRESS_FILE" ]]; then
    return
  fi

  cat > "$PROGRESS_FILE" <<'EOF'
# Ralph Progress Log

## Codebase Patterns
- 기술 블로그의 기본 품질 체크는 `bundle exec jekyll build`다.

Started: manual bootstrap
---
EOF
}

archive_if_branch_changed() {
  local current_branch=""
  local last_branch=""
  local folder_name=""
  local archive_folder=""

  if [[ ! -f "$PRD_FILE" || ! -f "$LAST_BRANCH_FILE" ]]; then
    return
  fi

  current_branch="$(jq -r '.branchName // empty' "$PRD_FILE" 2>/dev/null || true)"
  last_branch="$(cat "$LAST_BRANCH_FILE" 2>/dev/null || true)"

  if [[ -z "$current_branch" || -z "$last_branch" || "$current_branch" == "$last_branch" ]]; then
    return
  fi

  folder_name="$(echo "$last_branch" | sed 's|^ralph/||')"
  archive_folder="$ARCHIVE_DIR/$(date +%Y-%m-%d)-$folder_name"

  echo "Archiving previous Ralph state: $last_branch"
  mkdir -p "$archive_folder"
  cp "$PRD_FILE" "$archive_folder/prd.json"
  [[ -f "$PROGRESS_FILE" ]] && cp "$PROGRESS_FILE" "$archive_folder/progress.txt"
}

track_current_branch() {
  local current_branch=""

  current_branch="$(jq -r '.branchName // empty' "$PRD_FILE" 2>/dev/null || true)"
  if [[ -n "$current_branch" ]]; then
    echo "$current_branch" > "$LAST_BRANCH_FILE"
  fi
}

run_iteration() {
  if [[ "$TOOL" == "amp" ]]; then
    require_command "amp"
    (
      cd "$PROJECT_ROOT"
      cat "$PROMPT_FILE" | amp --dangerously-allow-all
    )
    return
  fi

  require_command "claude"
  (
    cd "$PROJECT_ROOT"
    claude --dangerously-skip-permissions --print < "$CLAUDE_FILE"
  )
}

require_command "git"
require_command "jq"
require_file "$PRD_FILE"
require_file "$PROMPT_FILE"
require_file "$CLAUDE_FILE"

if ! git -C "$PROJECT_ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Error: Ralph must run inside a git repository."
  exit 1
fi

initialize_progress_file
archive_if_branch_changed
track_current_branch

echo "Starting Ralph loop"
echo "Project root: $PROJECT_ROOT"
echo "Tool: $TOOL"
echo "Max iterations: $MAX_ITERATIONS"

for iteration in $(seq 1 "$MAX_ITERATIONS"); do
  echo ""
  echo "==============================================================="
  echo "  Ralph Iteration $iteration of $MAX_ITERATIONS ($TOOL)"
  echo "==============================================================="

  output="$(run_iteration 2>&1 | tee /dev/stderr || true)"

  if echo "$output" | grep -q "<promise>COMPLETE</promise>"; then
    echo ""
    echo "Ralph completed all tasks."
    exit 0
  fi

  echo "Iteration $iteration complete."
  sleep 2
done

echo ""
echo "Ralph reached max iterations ($MAX_ITERATIONS) without completing all tasks."
echo "Check $PROGRESS_FILE for the latest status."
exit 1
