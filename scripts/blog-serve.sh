#!/usr/bin/env bash
# serve도 build와 같은 locale/rbenv 조건으로 실행해야 로컬과 배포 차이를 줄일 수 있다.

set -euo pipefail

export LANG="${LANG:-en_US.UTF-8}"
export LC_ALL="${LC_ALL:-en_US.UTF-8}"

if command -v rbenv >/dev/null 2>&1; then
  eval "$(rbenv init - bash)"
fi

bundle exec jekyll serve --livereload "$@"
