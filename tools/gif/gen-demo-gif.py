#!/usr/bin/env python3
"""screenpath demo on a NEUTRAL, self-drawn mock landing page (no real brand)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "docs", "demo.gif")
W, H = 960, 561

HN   = "/System/Library/Fonts/HelveticaNeue.ttc"
MONO = "/System/Library/Fonts/Menlo.ttc"
f_cap     = ImageFont.truetype(HN, 19, index=0)
f_cap_b   = ImageFont.truetype(HN, 19, index=1)
f_toast_t = ImageFont.truetype(HN, 16, index=1)
f_toast_s = ImageFont.truetype(HN, 14, index=0)
f_toast_now = ImageFont.truetype(HN, 12, index=0)
f_badge   = ImageFont.truetype(HN, 13, index=0)
f_term_t  = ImageFont.truetype(HN, 12, index=0)
f_mono    = ImageFont.truetype(MONO, 16)
f_mono_b  = ImageFont.truetype(MONO, 16, index=1)
f_mono_path = ImageFont.truetype(MONO, 11)
# page fonts
f_nav   = ImageFont.truetype(HN, 14, index=0)
f_logo  = ImageFont.truetype(HN, 16, index=1)
f_h1    = ImageFont.truetype(HN, 33, index=1)
f_sub   = ImageFont.truetype(HN, 15, index=0)
f_btn   = ImageFont.truetype(HN, 14, index=1)
f_feat  = ImageFont.truetype(HN, 13, index=1)

CYAN   = (86, 212, 221)
ACCENT = (99, 102, 241)
ACC2   = (6, 182, 212)
INK    = (17, 24, 39)
GRAYTX = (107, 114, 128)
LINE   = (229, 231, 235)
CWm = f_mono.getbbox("M")[2] - f_mono.getbbox("M")[0]

SEL = (488, 112, 904, 430)   # the hero illustration card


def rounded(d, box, r, **kw):
    d.rounded_rectangle(box, radius=r, **kw)


def make_bg():
    img = Image.new("RGB", (W, H), (245, 246, 248))
    d = ImageDraw.Draw(img)
    # top nav
    d.rectangle([0, 0, W, 52], fill=(255, 255, 255))
    d.line([(0, 52), (W, 52)], fill=LINE, width=1)
    d.ellipse([24, 18, 44, 38], fill=ACCENT)
    d.text((52, 23), "Acme", font=f_logo, fill=INK)
    x = 150
    for it in ("Overview", "Features", "Pricing", "Docs", "Blog"):
        d.text((x, 25), it, font=f_nav, fill=GRAYTX)
        x += d.textlength(it, font=f_nav) + 26
    rounded(d, [W - 108, 14, W - 24, 40], 13, fill=ACCENT)
    d.text((W - 90, 22), "Sign in", font=f_nav, fill=(255, 255, 255))
    # hero text (left)
    d.text((60, 120), "Build once.", font=f_h1, fill=INK)
    d.text((60, 162), "Ship everywhere.", font=f_h1, fill=INK)
    d.text((60, 224), "A tiny toolkit for people who live", font=f_sub, fill=GRAYTX)
    d.text((60, 247), "in the terminal. No bloat, no lock-in.", font=f_sub, fill=GRAYTX)
    rounded(d, [60, 296, 196, 334], 8, fill=ACCENT)
    d.text((90, 306), "Get started", font=f_btn, fill=(255, 255, 255))
    rounded(d, [208, 296, 330, 334], 8, outline=LINE, width=1)
    d.text((232, 306), "Learn more", font=f_btn, fill=GRAYTX)
    # hero illustration card (gradient + abstract shapes)
    cx0, cy0, cx1, cy1 = SEL
    grad = Image.new("RGB", (cx1 - cx0, cy1 - cy0))
    gd = ImageDraw.Draw(grad)
    hh = cy1 - cy0
    for yy in range(hh):
        t = yy / hh
        col = tuple(int(ACCENT[k] + (ACC2[k] - ACCENT[k]) * t) for k in range(3))
        gd.line([(0, yy), (cx1 - cx0, yy)], fill=col)
    mask = Image.new("L", grad.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, grad.size[0] - 1, grad.size[1] - 1], radius=18, fill=255)
    img.paste(grad, (cx0, cy0), mask)
    od = ImageDraw.Draw(img, "RGBA")
    od.ellipse([cx0 + 36, cy0 + 44, cx0 + 168, cy0 + 176], fill=(255, 255, 255, 55))
    od.ellipse([cx1 - 175, cy1 - 165, cx1 - 45, cy1 - 35], fill=(255, 255, 255, 38))
    rounded(od, [cx0 + 120, cy0 + 110, cx0 + 300, cy0 + 210], 16, fill=(255, 255, 255, 70))
    rounded(od, [cx0 + 140, cy0 + 132, cx0 + 250, cy0 + 146], 7, fill=(255, 255, 255, 130))
    rounded(od, [cx0 + 140, cy0 + 158, cx0 + 220, cy0 + 170], 6, fill=(255, 255, 255, 90))
    # bottom feature cards
    for i in range(3):
        fx = 60 + i * 300
        rounded(d, [fx, 462, fx + 262, 540], 12, fill=(255, 255, 255), outline=LINE, width=1)
        d.ellipse([fx + 18, 480, fx + 44, 506], fill=(199, 210, 254))
        d.text((fx + 56, 482), "Feature " + str(i + 1), font=f_feat, fill=INK)
        d.text((fx + 56, 504), "Fast, simple, yours.", font=ImageFont.truetype(HN, 12), fill=GRAYTX)
    return img


bg = make_bg()


def dtext_ls(d, xy, text, font, fill, ls=0.0):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + ls
    return x


def dim_outside(base, rect, alpha=120):
    ov = Image.new("RGBA", base.size, (0, 0, 0, alpha))
    ImageDraw.Draw(ov).rectangle(rect, fill=(0, 0, 0, 0))
    return Image.alpha_composite(base.convert("RGBA"), ov).convert("RGB")


def crosshair(d, x, y):
    d.line([(x - 12, y), (x + 12, y)], fill=(255, 255, 255), width=3)
    d.line([(x, y - 12), (x, y + 12)], fill=(255, 255, 255), width=3)
    d.line([(x - 12, y), (x + 12, y)], fill=(45, 45, 45), width=1)
    d.line([(x, y - 12), (x, y + 12)], fill=(45, 45, 45), width=1)


def selection(d, rect, badge=True):
    x0, y0, x1, y1 = rect
    d.rectangle((x0 - 1, y0 - 1, x1 + 1, y1 + 1), outline=(35, 35, 35), width=1)
    d.rectangle(rect, outline=(255, 255, 255), width=2)
    if badge:
        label = f"{x1 - x0} x {y1 - y0}"
        tw = d.textlength(label, font=f_badge)
        bx, by = x0 + 6, y1 + 8
        rounded(d, [bx, by, bx + tw + 16, by + 22], 5, fill=(0, 0, 0, 230))
        d.text((bx + 8, by + 4), label, font=f_badge, fill=(255, 255, 255))


def caption(img, head, text):
    d = ImageDraw.Draw(img, "RGBA")
    hw = d.textlength(head + "  ", font=f_cap_b)
    tw = dtext_ls(ImageDraw.Draw(Image.new("RGB", (10, 10))), (0, 0), text, f_cap, (0, 0, 0), 0.3)
    bw = hw + tw + 36
    bx = (W - bw) / 2
    by = H - 56
    rounded(d, [bx, by, bx + bw, by + 38], 19, fill=(18, 20, 24, 240))
    x = bx + 18
    x = dtext_ls(d, (x, by + 9), head + "  ", f_cap_b, (255, 255, 255), 0.3)
    dtext_ls(d, (x, by + 9), text, f_cap, (225, 228, 232), 0.3)
    return img


def toast(img, slide=1.0):
    d = ImageDraw.Draw(img, "RGBA")
    tw_, th_ = 330, 80
    full_x = W - tw_ - 18
    x = int(full_x + (1 - slide) * (tw_ + 30))
    y = 18
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([x, y, x + tw_, y + th_], radius=16, fill=(0, 0, 0, 80))
    sh = sh.filter(ImageFilter.GaussianBlur(9))
    img.paste(Image.alpha_composite(img.convert("RGBA"), sh).convert("RGB"))
    d = ImageDraw.Draw(img, "RGBA")
    rounded(d, [x, y, x + tw_, y + th_], 16, fill=(248, 249, 251, 253))
    ix, iy = x + 15, y + 17
    rounded(d, [ix, iy, ix + 46, iy + 46], 11, fill=(28, 33, 40, 255))
    d.text((ix + 10, iy + 12), ">_", font=f_mono_b, fill=CYAN + (255,))
    tx = ix + 60
    dtext_ls(d, (tx, y + 13), "screenpath", f_toast_t, (22, 24, 28, 255), 0.4)
    dtext_ls(d, (x + tw_ - 50, y + 15), "now", f_toast_now, (150, 154, 160, 255), 0.3)
    dtext_ls(d, (tx, y + 33), "Path copied to clipboard", f_toast_s, (55, 60, 67, 255), 0.4)
    d.text((tx, y + 53), "~/Screenshots/shot-20260606-143012.png",
           font=f_mono_path, fill=(120, 126, 134, 255))
    return img


def terminal(img, rise=1.0, prompt_path="", prompt_q="", show_paste=False, cursor=True):
    tw_, th_ = 700, 196
    tx = (W - tw_) // 2
    full_y = H - th_ - 64
    ty = int(full_y + (1 - rise) * (th_ + 90))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([tx, ty, tx + tw_, ty + th_], radius=12, fill=(0, 0, 0, 130))
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    img.paste(Image.alpha_composite(img.convert("RGBA"), sh).convert("RGB"))
    d = ImageDraw.Draw(img, "RGBA")
    rounded(d, [tx, ty, tx + tw_, ty + th_], 12, fill=(13, 17, 23, 255))
    rounded(d, [tx, ty, tx + tw_, ty + 32], 12, fill=(38, 44, 54, 255))
    d.rectangle([tx, ty + 20, tx + tw_, ty + 32], fill=(38, 44, 54, 255))
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        cx = tx + 18 + i * 18
        d.ellipse([cx - 5, ty + 11, cx + 5, ty + 21], fill=c)
    tt = "claude code  -  zsh"
    dtext_ls(d, (tx + (tw_ - d.textlength(tt, font=f_term_t)) / 2 - 6, ty + 9),
             tt, f_term_t, (160, 166, 175, 255), 0.3)
    cy, cx = ty + 56, tx + 20
    d.text((cx, cy), "> ", font=f_mono_b, fill=(88, 166, 255, 255))
    x = cx + d.textlength("> ", font=f_mono)
    if show_paste and not prompt_path:
        bx = x
        for k in (" Cmd ", " V "):
            kw = d.textlength(k, font=f_mono) + 6
            rounded(d, [bx, cy - 1, bx + kw, cy + 21], 5, fill=(40, 46, 55, 255), outline=(84, 90, 100, 255))
            d.text((bx + 3, cy + 1), k, font=f_mono, fill=(205, 211, 219, 255))
            bx += kw + 8
    if prompt_path:
        d.text((x, cy), prompt_path, font=f_mono, fill=CYAN + (255,))
        x += d.textlength(prompt_path, font=f_mono)
    if prompt_q:
        d.text((x, cy), prompt_q, font=f_mono, fill=(230, 234, 238, 255))
        x += d.textlength(prompt_q, font=f_mono)
    if cursor and (prompt_path or not show_paste):
        d.rectangle([x + 1, cy + 1, x + 1 + CWm, cy + 20], fill=(230, 234, 238, 255))
    return img


PATH = "~/Screenshots/shot-20260606-143012.png"
Q = "  what's off in this layout?"
frames, durs = [], []


def add(img, ms):
    frames.append(img.convert("RGB")); durs.append(ms)


def black_blend(a):
    return Image.blend(bg, Image.new("RGB", bg.size, (0, 0, 0)), a)


# SCENE 1: drag select
sx, sy = SEL[0], SEL[1]
im = bg.copy(); crosshair(ImageDraw.Draw(im), sx, sy)
add(caption(im, "1", "drag to select a region"), 600)
steps = 6
for i in range(1, steps + 1):
    t = i / steps
    ex = int(sx + (SEL[2] - sx) * t); ey = int(sy + (SEL[3] - sy) * t)
    rect = (sx, sy, ex, ey)
    im = dim_outside(bg, rect)
    dd = ImageDraw.Draw(im, "RGBA"); selection(dd, rect, badge=(i == steps)); crosshair(dd, ex, ey)
    add(caption(im, "1", "drag to select a region"), 95)
im = dim_outside(bg, SEL)
selection(ImageDraw.Draw(im, "RGBA"), SEL)
add(caption(im, "1", "drag to select a region"), 550)

# SCENE 2: shutter + toast
add(black_blend(0.5), 55); add(black_blend(0.16), 55)
for s in (0.0, 0.5, 1.0):
    add(caption(toast(bg.copy(), slide=s), "2", "the file PATH is copied to your clipboard"), 110 if s < 1 else 250)
add(caption(toast(bg.copy(), slide=1.0), "2", "the file PATH is copied to your clipboard"), 1100)

# SCENE 3: terminal paste
for r in (0.0, 0.55, 1.0):
    im = terminal(toast(bg.copy(), slide=1.0), rise=r)
    add(caption(im, "3", "paste it into your terminal / agent"), 110 if r < 1 else 350)
im = terminal(toast(bg.copy(), slide=1.0), rise=1.0, show_paste=True, cursor=False)
add(caption(im, "3", "paste it into your terminal / agent  ( Cmd + V )"), 550)
im = terminal(toast(bg.copy(), slide=1.0), rise=1.0, prompt_path=PATH)
add(caption(im, "3", "paste it into your terminal / agent"), 700)
for i in range(2, len(Q) + 1, 2):
    im = terminal(toast(bg.copy(), slide=1.0), rise=1.0, prompt_path=PATH, prompt_q=Q[:i])
    add(caption(im, "3", "paste it into your terminal / agent"), 48)
for blink in (True, False, True, False, True):
    im = terminal(toast(bg.copy(), slide=1.0), rise=1.0, prompt_path=PATH, prompt_q=Q, cursor=blink)
    add(caption(im, "done", "no more screenshots stuck in your clipboard"), 450)

# encode
sample = Image.new("RGB", (W, H * 3))
sample.paste(frames[3], (0, 0)); sample.paste(frames[16], (0, H)); sample.paste(frames[-1], (0, H * 2))
pal = sample.convert("P", palette=Image.ADAPTIVE, colors=200)
q = [fr.quantize(palette=pal, dither=Image.FLOYDSTEINBERG) for fr in frames]
q[0].save(OUT, save_all=True, append_images=q[1:], duration=durs, loop=0, disposal=1, optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes,", len(frames), "frames")
