#!/usr/bin/env python3
"""Terminal-style usage GIF for screenpath: typed commands + output."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 860, 384
BAR = 30
PADX, TOP = 22, BAR + 16
LH = 25

BG    = (13, 17, 23)
BARBG = (32, 38, 47)
PROMPT= (63, 185, 80)
CMD   = (230, 234, 238)
CYAN  = (86, 212, 221)
GRAY  = (132, 139, 149)
OKG   = (88, 196, 120)

MONO = "/System/Library/Fonts/Menlo.ttc"
HN   = "/System/Library/Fonts/HelveticaNeue.ttc"
f   = ImageFont.truetype(MONO, 15)
fb  = ImageFont.truetype(MONO, 15, index=1)
ft  = ImageFont.truetype(HN, 12, index=0)
CW  = f.getbbox("M")[2] - f.getbbox("M")[0]

# Transcript: ('cmd', text) typed out; ('out', [(text,color),...]) shown at once.
SCRIPT = [
    ('cmd', 'screenpath'),
    ('out', [('~/Screenshots/shot-20260606-143012.png', CYAN), ('   # copied to clipboard', GRAY)]),
    ('cmd', 'screenpath --quote      # path with spaces? keep it one arg'),
    ('out', [("'~/My Shots/shot-20260606-143015.png'", CYAN)]),
    ('cmd', 'screenpath --link       # also repoint ~/Screenshots/latest.png'),
    ('out', [('~/Screenshots/shot-20260606-143020.png', CYAN)]),
    ('cmd', 'claude "what is wrong in ~/latest.png?"'),
    ('out', [('  (your agent reads the screenshot by path)', GRAY)]),
]


def render(done_lines, typing=None, cursor=True):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, BAR], fill=BARBG)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        cx = 18 + i * 16
        d.ellipse([cx - 5, BAR // 2 - 5, cx + 5, BAR // 2 + 5], fill=c)
    title = "screenpath  -  zsh"
    d.text(((W - d.textlength(title, font=ft)) / 2, BAR // 2 - 8), title, font=ft, fill=GRAY)

    y = TOP
    for kind, payload in done_lines:
        if kind == 'cmd':
            d.text((PADX, y), "$ ", font=fb, fill=PROMPT)
            x = PADX + d.textlength("$ ", font=f)
            # color a trailing "# comment" gray
            if '#' in payload:
                cmd_part, com = payload.split('#', 1)
                d.text((x, y), cmd_part, font=f, fill=CMD)
                x += d.textlength(cmd_part, font=f)
                d.text((x, y), '#' + com, font=f, fill=GRAY)
            else:
                d.text((x, y), payload, font=f, fill=CMD)
        else:
            x = PADX
            for text, color in payload:
                d.text((x, y), text, font=f, fill=color)
                x += d.textlength(text, font=f)
        y += LH

    if typing is not None:
        d.text((PADX, y), "$ ", font=fb, fill=PROMPT)
        x = PADX + d.textlength("$ ", font=f)
        shown = typing
        if '#' in shown:
            cmd_part, com = shown.split('#', 1)
            d.text((x, y), cmd_part, font=f, fill=CMD)
            x += d.textlength(cmd_part, font=f)
            d.text((x, y), '#' + com, font=f, fill=GRAY)
        else:
            d.text((x, y), shown, font=f, fill=CMD)
            x += d.textlength(shown, font=f)
        if cursor:
            d.rectangle([x + 1, y + 2, x + 1 + CW, y + 19], fill=CMD)
    return img


frames, durs = [], []
def add(im, ms): frames.append(im); durs.append(ms)

done = []
add(render(done, typing="", cursor=True), 500)
for kind, payload in SCRIPT:
    if kind == 'cmd':
        for i in range(1, len(payload) + 1, 2):
            add(render(done, typing=payload[:i]), 38)
        add(render(done, typing=payload), 250)          # finished typing
        done.append(('cmd', payload))
        add(render(done, typing=None, cursor=False), 180)  # "enter"
    else:
        done.append(('out', payload))
        add(render(done, typing=None, cursor=False), 650)
# final hold with a fresh blinking prompt
for blink in (True, False, True, False):
    add(render(done, typing="", cursor=blink), 450)

pal = frames[len(frames)//2].convert("P", palette=Image.ADAPTIVE, colors=48)
q = [im.quantize(palette=pal, dither=Image.NONE) for im in frames]
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "docs", "usage.gif")
q[0].save(out, save_all=True, append_images=q[1:], duration=durs, loop=0, disposal=1, optimize=True)
print("wrote", out, os.path.getsize(out), "bytes,", len(frames), "frames")
