#!/usr/bin/env bash
#
# Dependency-free test suite for screenpath.
# Runs on Linux or macOS — it tests argument parsing and path formatting, neither
# of which needs an actual screen capture, so it works on headless CI runners.

set -u

HERE="$(cd "$(dirname "$0")/.." && pwd)"
SP="$HERE/bin/screenpath"
pass=0 fail=0

check() { # desc  actual  expected
  if [ "$2" = "$3" ]; then
    pass=$((pass + 1))
  else
    fail=$((fail + 1))
    printf 'FAIL: %s\n  got:      [%s]\n  expected: [%s]\n' "$1" "$2" "$3"
  fi
}

# Load the helpers (the script returns early when sourced).
# shellcheck source=bin/screenpath disable=SC1091
source "$SP"

# --- behavioural: run as a subprocess (exits before any capture) ---
check "--version prints name and version" "$("$SP" --version)" "screenpath $VERSION"

"$SP" --help  >/dev/null 2>&1; check "--help exits 0"          "$?" "0"
"$SP" --setup >/dev/null 2>&1; check "--setup exits 0"         "$?" "0"
"$SP" --nope  >/dev/null 2>&1; check "unknown option exits 2"  "$?" "2"

# --- install-raycast subcommand (pure file copy, no capture needed) ---
"$SP" install-raycast >/dev/null 2>&1
check "install-raycast with no dir exits 0" "$?" "0"

rc_dir="$(mktemp -d)"
"$SP" install-raycast "$rc_dir" >/dev/null 2>&1
check "install-raycast copies the script" \
  "$( [ -f "$rc_dir/screenpath.sh" ] && echo yes || echo no )" "yes"
rm -rf "$rc_dir"

"$SP" install-raycast /no/such/dir >/dev/null 2>&1
check "install-raycast with a bad dir exits 1" "$?" "1"

# --- unit: pure path-formatting helpers ---
FORMAT=raw
check "raw passes the path through unchanged" \
  "$(format_path '/tmp/a b/c.png')" '/tmp/a b/c.png'

FORMAT=quote
roundtrip=""
quoted="$(format_path "/tmp/it's a shot.png")"
eval "roundtrip=$quoted"          # a correct shell-quote survives re-parsing
check "quote round-trips through the shell" "$roundtrip" "/tmp/it's a shot.png"

FORMAT=url
check "url percent-encodes spaces" \
  "$(format_path '/tmp/a b.png')" 'file:///tmp/a%20b.png'
check "url percent-encodes non-ASCII (UTF-8)" \
  "$(format_path '/tmp/그림.png')" 'file:///tmp/%EA%B7%B8%EB%A6%BC.png'

# --- update_link helper (filesystem only) ---
ld="$(mktemp -d)"
: > "$ld/shot.png"
update_link "$ld/shot.png" "$ld/latest.png"
check "update_link creates a symlink"      "$( [ -L "$ld/latest.png" ] && echo yes || echo no )" "yes"
check "symlink points at the capture"      "$(readlink "$ld/latest.png")" "$ld/shot.png"
: > "$ld/shot2.png"
update_link "$ld/shot2.png" "$ld/latest.png"
check "update_link repoints an existing link" "$(readlink "$ld/latest.png")" "$ld/shot2.png"
: > "$ld/real.png"
update_link "$ld/shot.png" "$ld/real.png" 2>/dev/null
check "update_link refuses to clobber a real file" "$?" "1"
rm -rf "$ld"

# --- capture_ms + pick_path (collision handling) ---
ms="$(capture_ms)"
ms_class=ok
[ -n "$ms" ] && case "$ms" in *[!0-9]*) ms_class=bad ;; esac
check "capture_ms is numeric or empty" "$ms_class" "ok"

pd="$(mktemp -d)"
check "pick_path returns the clean base when free" \
  "$(pick_path "$pd" shot 20260606-120000)" "$pd/shot-20260606-120000.png"
: > "$pd/shot-20260606-120000.png"
capture_ms() { printf ''; }      # force the deterministic -N counter path
check "pick_path adds -2 on first collision" \
  "$(pick_path "$pd" shot 20260606-120000)" "$pd/shot-20260606-120000-2.png"
: > "$pd/shot-20260606-120000-2.png"
check "pick_path adds -3 on next collision" \
  "$(pick_path "$pd" shot 20260606-120000)" "$pd/shot-20260606-120000-3.png"
rm -rf "$pd"

printf '\n%d passed, %d failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ]
