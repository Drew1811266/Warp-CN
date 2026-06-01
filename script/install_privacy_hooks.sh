#!/bin/sh
set -eu

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

chmod +x .githooks/pre-commit \
  .githooks/pre-push \
  .githooks/post-commit \
  .githooks/post-checkout \
  .githooks/post-merge

git config core.hooksPath .githooks
printf '%s\n' "Installed privacy guard hooks via core.hooksPath=.githooks"
