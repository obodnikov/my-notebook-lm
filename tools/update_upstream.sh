#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
echo "Fetching latest upstream..."
git fetch upstream

echo "Updating vendor copy..."
git rm -r upstream/app
git read-tree --prefix=upstream/app -u upstream/main
git commit -m "Update vendor to latest upstream"

# inside update_upstream.sh
echo "Reapplying downstream patches..."
find patches -type f -name '*.patch' | sort | while read -r p; do
  echo "Applying $p..."
  if git apply --check "$p"; then
    git apply "$p"
  else
    echo "⚠️ Conflict applying $p — manual resolution required."
    exit 1
  fi
done


git commit -am "Reapply downstream patchset"
echo "✅ Upstream update complete."
