# GIF generators (dev only)

These scripts regenerate the README animations. They are not part of the tool and
are not installed by Homebrew.

- `gen-demo-gif.py`  → `docs/demo.gif` (the workflow demo over a self-drawn,
  brand-free mock landing page)
- `gen-usage-gif.py` → `docs/usage.gif` (a terminal showing example commands)

## Run

```sh
python3 -m venv /tmp/gifvenv && /tmp/gifvenv/bin/pip install Pillow
/tmp/gifvenv/bin/python tools/gif/gen-demo-gif.py
/tmp/gifvenv/bin/python tools/gif/gen-usage-gif.py
```

Requires Pillow and macOS system fonts (Helvetica Neue, Menlo). Output is
deterministic — re-running produces byte-identical GIFs.
