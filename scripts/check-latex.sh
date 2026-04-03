#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
docs_dir="$repo_root/docs"
log_file="$docs_dir/out/main.log"

cd "$docs_dir"
latexmk -lualatex -interaction=nonstopmode -halt-on-error -file-line-error -outdir=out main.tex

if rg -n "Reference .* undefined|Citation .* undefined|There were undefined references|There were undefined citations" "$log_file"; then
    exit 1
fi
