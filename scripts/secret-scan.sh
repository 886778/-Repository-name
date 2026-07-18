#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$project_root"

exclude=(
  --hidden
  --glob '!**/.git/**'
  --glob '!**/.venv/**'
  --glob '!**/node_modules/**'
  --glob '!**/.next/**'
  --glob '!**/__pycache__/**'
  --glob '!scripts/secret-scan.sh'
)

patterns=(
  '-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----'
  'github_pat_[A-Za-z0-9_]{20,}'
  'gh[pousr]_[A-Za-z0-9_]{20,}'
  'AKIA[0-9A-Z]{16}'
  'sk-[A-Za-z0-9]{32,}'
)

found=0
for pattern in "${patterns[@]}"; do
  if rg --line-number "${exclude[@]}" -- "$pattern" .; then
    found=1
  fi
done

if [[ "$found" -ne 0 ]]; then
  echo "Potential secret detected." >&2
  exit 1
fi

echo "Secret scan passed."
