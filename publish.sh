# This script pushes the contents in build/ directory to the static branch.
# Raymond Kil, September 2025 (jkil@nd.edu)

#!/bin/bash
set -e # stop if any command fails
git checkout static

git rm -rf . >/dev/null 2>&1 || true
git clean -fdx >/dev/null 2>&1 || true
cp -R build/* .
touch .nojekyll