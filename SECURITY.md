# Security

screenpath asks for **Screen Recording** permission, so it should be easy to trust.
Here is exactly what it is and does.

## What it is

- **One Bash file** — [`bin/screenpath`](bin/screenpath), ~350 lines. Read it; that's
  the whole tool. The only other shipped files are shell completions and a Raycast
  helper script.
- **No dependencies** beyond what macOS already ships (`screencapture`, `pbcopy`,
  `osascript`, `date`, `perl`).

## What it does NOT do

- **No network access.** It makes zero network calls — no analytics, no telemetry,
  no update checks, nothing phones home.
- **No background process**, no daemon, no menu-bar agent. It runs once per capture
  and exits.
- It only reads the screen when *you* trigger a capture, and only writes screenshot
  files to your chosen directory (default `~/Screenshots`).

## Permissions

The **Screen Recording** permission is macOS's requirement for *any* tool that takes a
screenshot — it is granted to the app that launches screenpath (Terminal, Raycast,
Shortcuts), not to screenpath specifically. screenpath asks for nothing beyond that.

## Filenames & untrusted input

Filenames are passed to `osascript` as arguments (never interpolated into AppleScript
source), and `$SCREENPATH_PREFIX` is rejected if it contains `/`. So a path with quotes
or separators cannot break the script or inject commands.

## Reporting a problem

Open an issue at https://github.com/truth0530/screenpath/issues (or mark it private if
you prefer). There is no formal SLA — this is a small personal project.
