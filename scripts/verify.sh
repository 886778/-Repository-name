#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$project_root"

if [[ -s "${NVM_DIR:-$HOME/.nvm}/nvm.sh" ]]; then
  # shellcheck source=/dev/null
  source "${NVM_DIR:-$HOME/.nvm}/nvm.sh"
  nvm use >/dev/null
fi

uv_bin="$(command -v uv || true)"
if [[ -z "$uv_bin" && -x "$HOME/.local/bin/uv" ]]; then
  uv_bin="$HOME/.local/bin/uv"
fi
if [[ -z "$uv_bin" ]]; then
  echo "uv is required" >&2
  exit 1
fi

[[ "$(node --version)" == "v24.18.0" ]]
[[ "$(pnpm --version)" == "11.9.0" ]]
[[ "$($uv_bin run python --version)" == "Python 3.14.6" ]]

"$uv_bin" lock --check
"$uv_bin" run ruff format --check apps packages tests
"$uv_bin" run ruff check apps packages tests
"$uv_bin" run mypy
"$uv_bin" run pytest --cov --cov-report=term-missing
"$uv_bin" run lint-imports

pnpm install --frozen-lockfile
pnpm format:check
pnpm lint
pnpm typecheck
pnpm test
pnpm architecture
pnpm build
