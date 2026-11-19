"""NOIR format B (François Louis, THEME b) : super déficit foncier 21 400 €, plus d'économie avec le plafond normal."""
import math, subprocess, sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import os
THEME = os.environ.get("THEME","b")
W, H, FPS = 1080, 1920, 30
AUDIO = float(os.environ["AUDIO"])
TAIL = float(os.environ.get("TAIL","2.0"))
DUR = AUDIO + TAIL
FD = "/home/claude/fonts/use/"
_fc = {}
def F(n, s):
    k = (n, s)
    if k not in _fc: _fc[k] = ImageFont.truetype(FD + n + ".woff", s)
    return _fc[k]
SERIF = lambda s: F("source-serif-4-latin-400-normal", s)
SERIF_I = lambda s: F("source-serif-4-latin-400-italic", s)
COND = lambda s: F("oswald-latin-600-normal", s)
MONO = lambda s: F("jetbrains-mono-latin-400-normal", s)

BG0 = (10, 10, 11); TXT = (236, 232, 222); DIM = (108, 106, 102); DIM2 = (64, 63, 61)
GOLD = (232, 194, 92); RED = (226, 86, 64); GREEN = (128, 196, 96); LIME = (198, 240, 107); BLUE = (110, 150, 230)
CHIP = (18, 18, 20); CHIPB = (40, 40, 43)
MX = 100

SEGS = [tuple(x) for x in json.load(open("segs.json"))]
WORDS = []
for s, e, txt in SEGS:
    ws = txt.split(); tot = sum(len(w) + 1 for w in ws); t = s
    for w in ws:
        d = (e - s) * (len(w) + 1) / tot; WORDS.append((t, t + d, w)); t += d

def cl(x): return max(0.0, min(1.0, x))
def eo(x): x = cl(x); return 1 - (1 - x) ** 3
def eio(x): x = cl(x); return x * x * (3 - 2 * x)
def back(x):
    x = cl(x); c1 = 1.70158; c3 = c1 + 1; return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def A(c, a): return tuple(c[:3]) + (int(255 * cl(a)),)
def eur(v): return f"{int(round(v)):,}".replace(",", " ") + " €"

def make_bg():
    bg = np.zeros((H, W, 3), dtype="int16") + np.array(BG0, dtype="int16")
    g = Image.new("RGB", (W, H)); gd = ImageDraw.Draw(g)
    if THEME == "a":
        gd.ellipse([W / 2 - 440, 620, W / 2 + 440, 1240], fill=(34, 28, 16))
    else:
        gd.ellipse([-380, 1050, 560, 2150], fill=(13, 34, 20))
        gd.ellipse([520, -300, 1500, 760], fill=(11, 19, 40))
        gd.ellipse([W / 2 - 380, 700, W / 2 + 380, 1200], fill=(14, 20, 18))
    g = np.asarray(g.filter(ImageFilter.GaussianBlur(190)), dtype="int16")
    im = Image.fromarray(np.clip(bg + g, 0, 255).astype("uint8"))
    d = ImageDraw.Draw(im); c = (34, 34, 34); L = 26
    for (x, y, sx, sy) in [(46, 46, 1, 1), (W - 46, 46, -1, 1), (46, H - 46, 1, -1), (W - 46, H - 46, -1, -1)]:
        d.line([x, y, x + sx * L, y], fill=c, width=2); d.line([x, y, x, y + sy * L], fill=c, width=2)
    return im.convert("RGBA")
BG = make_bg()

def win(t, s, e, fin=0.3, fout=0.3):
    if t < s or t > e + fout: return 0
    return min(1 if s == 0 else eo((t - s) / fin), 1 - eio((t - e) / fout))

def label(d, txt, sub, a):
    d.text((MX, 214), txt, font=MONO(23), fill=A(DIM, a))
    d.text((MX, 248), sub, font=MONO(19), fill=A(DIM2, a))

def chip(d, x, y, w, h, lab, val, col, a, vsize=48, vfont=None):
    d.rectangle([x, y, x + w, y + h], fill=A(CHIP, a), outline=A(CHIPB, a), width=2)
    d.text((x + 22, y + 16), lab, font=MONO(18), fill=A(DIM, a))
    d.text((x + 22, y + 46), val, font=(vfont or SERIF)(vsize), fill=A(col, a))

def bill(L, x, y, w, h, col, a=1, rot=0):
    b = Image.new("RGBA", (w + 4, h + 4), (0, 0, 0, 0)); bd = ImageDraw.Draw(b)
    bd.rectangle([1, 1, w, h], fill=A(tuple(int(c * 0.55) for c in col), a), outline=A(col, a), width=2)
    bd.ellipse([w / 2 - h * .28, h / 2 - h * .28, w / 2 + h * .28, h / 2 + h * .28], outline=A(col, a * .9), width=2)
    if rot: b = b.rotate(rot, expand=True, resample=Image.BICUBIC)
    L.alpha_composite(b, (int(x), int(y)))

def captions(L, d, t):
    if t > AUDIO + 0.2: return
    cur = None
    for i, (s, e, _) in enumerate(SEGS):
        if t >= s - 0.05: cur = i
    if cur is None: return
    s, e, _ = SEGS[cur]
    if t > e + 0.6: return
    words = [w for w in WORDS if s - 1e-6 <= w[0] < e]
    f = COND(48)
    lines, line, lw = [], [], 0
    for w in words:
        ww = d.textlength(w[2] + " ", font=f)
        if lw + ww > 860 and line: lines.append(line); line, lw = [], 0
        line.append(w); lw += ww
    if line: lines.append(line)
    y = 1440
    for ln in lines[:3]:
        total = sum(d.textlength(w[2] + " ", font=f) for w in ln)
        x = W / 2 - total / 2
        for ws, we, w in ln:
            if THEME == "b" and ws <= t < we + 0.05:
                tw = d.textlength(w, font=f)
                d.rounded_rectangle([x - 8, y - 2, x + tw + 8, y + 64], 10, fill=(198, 240, 107, 255))
                d.text((x, y), w, font=f, fill=(12, 12, 12))
            else:
                d.text((x, y), w, font=f, fill=TXT if t >= ws else (96, 94, 90))
            x += d.textlength(w + " ", font=f)
        y += 64


def run(SCENES, STARTS, voice):
    def frame(t):
        img = BG.copy(); L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        for sc in SCENES: sc(L, d, t)
        st = max(x for x in STARTS if x <= t); k = t - st
        z = 1 + 0.012 * min(k, 5) / 5
        if THEME == "b" and st > 0: z += 0.07 * (1 - eo(k / 0.45))
        if abs(z - 1) > 1e-3:
            Z = L.resize((int(W * z), int(H * z)), Image.BILINEAR)
            L = Z.crop((int((Z.width - W) / 2), int((Z.height - H) / 2), int((Z.width - W) / 2) + W, int((Z.height - H) / 2) + H))
        C = Image.new("RGBA", (W, H), (0, 0, 0, 0)); captions(C, ImageDraw.Draw(C), t)
        img.alpha_composite(L); img.alpha_composite(C); return img.convert("RGB")
    if sys.argv[1:2] == ["stills"]:
        ims = [frame(float(x)) for x in sys.argv[2:]]
        sh = Image.new("RGB", (360 * len(ims), 640))
        for i, im in enumerate(ims): sh.paste(im.resize((360, 640)), (360 * i, 0))
        sh.save("contact.png"); return
    out = sys.argv[1]; n = int(DUR * FPS)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-i", voice, "-filter_complex", f"[1:a]apad=pad_dur={TAIL}[a]",
                          "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                          "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", str(DUR), "-movflags", "+faststart", out],
                         stdin=subprocess.PIPE)
    for i in range(n): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print("ok", n)
