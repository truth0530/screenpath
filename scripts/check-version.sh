#!/usr/bin/env bash
#
# Guard against the script's VERSION drifting from the released git tag.
# At a tagged (release) commit the tag must equal "v$VERSION"; otherwise it skips.

set -euo pipefail

HERE="$(cd "$(dirname "$0")/.." && pwd)"
ver="$(bash "$HERE/bin/screenpath" --version | awk '{print $2}')"

tag="$(git -C "$HERE" describe --tags --exact-match HEAD 2>/dev/null || true)"
if [ -z "$tag" ]; then
  echo "HEAD is not a release tag; skipping (VERSION=$ver)"
  exit 0
fi

if [ "$tag" != "v$ver" ]; then
  echo "version mismatch: git tag is $tag but the script reports $ver" >&2
  echo "bump VERSION in bin/screenpath to match the tag before releasing." >&2
  exit 1
fi

echo "version OK: $tag == v$ver"
