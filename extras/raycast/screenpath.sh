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

# Use the brew-installed screenpath; fall back to PATH lookup.
if command -v screenpath >/dev/null 2>&1; then
  screenpath
else
  "$(brew --prefix 2>/dev/null)/bin/screenpath"
fi
