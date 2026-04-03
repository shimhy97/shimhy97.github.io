#!/usr/bin/env bash
# 원격 테마의 SCSS를 안정적으로 읽도록 UTF-8 locale을 강제로 맞춘다.
# 로컬 쉘 초기화 여부와 무관하게 rbenv Ruby를 잡아 빌드 명령이 흔들리지 않게 한다.

set -euo pipefail

export LANG="${LANG:-en_US.UTF-8}"
export LC_ALL="${LC_ALL:-en_US.UTF-8}"

if command -v rbenv >/dev/null 2>&1; then
  eval "$(rbenv init - bash)"
fi

bundle exec jekyll build "$@"
