#!/usr/bin/env bash
#
# Raycast Script Command for screenpath.
# Copy this file into your Raycast Script Commands directory, then assign a Hotkey
# to it in Raycast. See: https://github.com/raycast/script-commands
#
# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Screenpath
# @raycast.mode silent
#
# Optional parameters:
# @raycast.packageName screenpath
#
# Documentation:
# @raycast.description Capture a region and copy the file path to the clipboard
# @raycast.author truth0530
# @raycast.authorURL https://github.com/truth0530

# Prefer screenpath on PATH; otherwise try the Homebrew prefix; else report clearly.
if command -v screenpath >/dev/null 2>&1; then
  screenpath
elif brew_prefix="$(brew --prefix 2>/dev/null)" && [ -x "$brew_prefix/bin/screenpath" ]; then
  "$brew_prefix/bin/screenpath"
else
  echo "screenpath not found. Install: brew install truth0530/tap/screenpath" >&2
  exit 1
fi
