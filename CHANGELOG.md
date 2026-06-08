# Changelog

All notable changes to this project are documented here.
The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- `SECURITY.md` (no network / no telemetry; what the tool does and doesn't do).
- README "Why I made this" section and a "prefer a shell alias?" snippet.
- Linux support tracked as an issue (#1).

## [0.1.3] - 2026-06-08

### Added
- Shell completions for bash and zsh (installed by the Homebrew formula).
- `CHANGELOG.md`.

## [0.1.2] - 2026-06-07

### Fixed
- Distinguish a real capture failure from a user cancel: `screencapture` exits 0
  even when it cannot write a file, so a missing file plus an error message now
  exits 1 instead of looking like a successful, silent cancel.
- `--full` captures the main display (`-m`) so exactly one predictable file is
  produced on multi-display setups.
- Reject a `--prefix` / `$SCREENPATH_PREFIX` containing `/` (prevented writing
  outside the screenshots directory).
- `mkdir`/`cd` use `--`, so a directory starting with `-` no longer misparses.
- A failed `pbcopy` now exits non-zero instead of being swallowed.

### Changed
- Documented the exit-status contract in `--help` and the README.
- Corrected the Raycast setup guidance (register a Script Commands directory in
  Raycast first — there is no default), used a non-colliding `skhd` example, and
  fixed the `--tmp` description.
- The Homebrew formula now prints caveats (Screen Recording permission, hotkey).

## [0.1.1] - 2026-06-07

### Security
- Pass filenames to `osascript` as arguments instead of interpolating them into
  the AppleScript source, so a path containing quotes can neither break the
  script nor inject `do shell script`.

### Fixed
- Resolve `--dir` to an absolute path (deterministic save location under hotkey
  launchers; well-formed `file://` URL for relative directories).
- A failed image copy now exits non-zero.
- Missing option values and contradictory flags exit 2.

### Changed
- Notifications are off by default (`--notify` / `SCREENPATH_NOTIFY=1` to enable),
  and show the value actually copied.
- `capture_ms` falls back to `$RANDOM` when perl is unavailable.
- CI now also runs on macOS (bash 3.2, the real runtime).

## [0.1.0] - 2026-06-06

Initial public release: capture a screen region (or window / full screen) and
copy the saved file path to the clipboard — for terminal, tmux, SSH, and
AI-agent workflows on macOS. Includes `--quote` / `--url` / `--link` / `--tmp` /
`--image`, an `install-raycast` helper, an empty-capture permission check, a
test suite, and CI.

[0.1.3]: https://github.com/truth0530/screenpath/releases/tag/v0.1.3
[0.1.2]: https://github.com/truth0530/screenpath/releases/tag/v0.1.2
[0.1.1]: https://github.com/truth0530/screenpath/releases/tag/v0.1.1
[0.1.0]: https://github.com/truth0530/screenpath/releases/tag/v0.1.0
