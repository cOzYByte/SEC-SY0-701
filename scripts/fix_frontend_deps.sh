#!/usr/bin/env bash
# Automated dependency fix script for macOS / Linux
set -euo pipefail
IFS=$'\n\t'

echo "=== dep-fix script starting ==="

command -v npm >/dev/null 2>&1 || { echo "npm not found. Install Node.js/npm and retry."; exit 1; }
command -v git >/dev/null 2>&1 || { echo "git not found. Install git and retry."; exit 1; }

# Ensure run from repo root
if [ ! -f package.json ]; then
  echo "package.json not found in current directory. Run this script from the project root."
  exit 1
fi

# Require clean working tree
if [ -n "$(git status --porcelain)" ]; then
  echo "Git working tree is not clean. Commit or stash changes and re-run."
  git status --porcelain
  exit 1
fi

BRANCH="dep-fixes-$(date +%Y%m%d%H%M%S)"
echo "Creating branch $BRANCH"
git checkout -b "$BRANCH"

echo "Installing current deps..."
npm install

echo "Saving pre-fix audit (audit-pre.json)"
npm audit --json > audit-pre.json || true

echo "Running npm audit fix (non-forced)..."
npm audit fix || true

echo "Updating package.json to latest safe versions using npm-check-updates"
npx npm-check-updates -u

echo "Installing updated deps..."
npm install

echo "Saving post-update audit (audit-post.json)"
npm audit --json > audit-post.json || true

# Optional force fix if --force supplied
if [ "${1:-}" = "--force" ]; then
  echo "Running npm audit fix --force (may introduce breaking changes)"
  npm audit fix --force || true
  npm install
  npm audit --json > audit-post-force.json || true
fi

# Try build if script exists
if npm run | grep -q "build"; then
  echo "Running build..."
  npm run build --if-present
fi

# Stage and commit lockfile + package.json changes
git add package.json package-lock.json yarn.lock package-lock.yaml || true

if git diff --staged --quiet; then
  echo "No dependency file changes to commit."
else
  git commit -m "chore(deps): run npm audit fix and update dependencies"
fi

git push -u origin "$BRANCH"

echo "=== Done. Branch pushed: $BRANCH ==="
echo "Review audit-pre.json and audit-post.json, run tests, and validate builds before merging."