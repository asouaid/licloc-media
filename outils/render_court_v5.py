"""Vidéo test courte (25 s) : 200 000 € Paris vs Grenoble. Hook visible dès l'image 1."""
import math, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import os
VOICE = os.environ.get("VOICE", "vic")
THEME = os.environ.get("THEME", "a")
W, H, FPS = 1080, 1920, 30
AUDIO = {"vic": 22.91, "fl": 24.53}[VOICE]
TAIL = 2.4
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
GOLD = (232, 194, 92); RED = (226, 86, 64); GREEN = (128, 196, 96); LIME = (198, 240, 107)
CHIP = (18, 18, 20); CHIPB = (40, 40, 43)
MX = 100

SEGS = [
 (0.00, 1.37, "200 000 €."),
 (1.68, 4.02, "À Paris, tu achètes 20 m²."),
 (4.22, 5.09, "À Grenoble…"),
 (5.30, 6.26, "77 m²."),
 (6.70, 7.28, "Et le loyer ?"),
 (7.72, 9.53, "650 € par mois à Paris."),
 (9.88, 11.29, "950 € à Grenoble."),
 (11.68, 14.82, "Plus de 3 600 € de loyers en plus chaque année…"),
 (15.15, 16.55, "pour la même somme investie."),
 (16.93, 19.93, "Investir là où tu habites, c'est souvent le choix le plus cher."),
 (20.19, 23.19, "Commente VILLE, et on t'envoie l'accès à notre newsletter gratuite."),
]
REF = [(a, b) for a, b, _ in SEGS]
_SIL = {"vic": [(1.27,1.61),(3.64,3.97),(4.83,5.09),(6.00,6.38),(6.96,7.42),(9.18,9.58),(11.00,11.39),(14.35,14.67),(16.02,16.40),(19.38,19.66)],
        "fl": [(1.36,1.80),(3.82,4.31),(5.12,5.39),(6.32,6.85),(7.43,7.86),(9.79,10.14),(11.64,12.03),(15.32,15.64),(16.94,17.50),(20.59,21.04)]}[VOICE]
_b = [0.0]
for a_, b_ in _SIL: _b += [a_, b_]
_b.append(AUDIO - 0.05)
NEW = [(_b[2*i], _b[2*i+1]) for i in range(len(SEGS))]
SEGS = [(n[0], n[1], t) for n, (_, _, t) in zip(NEW, SEGS)]
TMAP = []
for (n0, n1), (o0, o1) in zip(NEW, REF): TMAP += [(n0, o0), (n1, o1)]
TMAP.append((AUDIO, 23.41)); TMAP.append((AUDIO + 10, 33.41))
def tmap(t):
    for (a0, b0), (a1, b1) in zip(TMAP, TMAP[1:]):
        if a0 <= t <= a1: return b0 if a1 == a0 else b0 + (b1 - b0) * (t - a0) / (a1 - a0)
    return t
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
def lerp(a, b, x): return a + (b - a) * x
def A(c, a): return tuple(c[:3]) + (int(255 * cl(a)),)
def eur(v): return f"{int(round(v)):,}".replace(",", " ") + " €"

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

# ---- Scène 1 : 200 000 € -> 20 m² vs 77 m² (visible dès t=0) ----
def floor(d, x0, y0, cols, n, filled, col, a, cell=34, gap=5):
    for i in range(n):
        r, c = divmod(i, cols)
        x = x0 + c * (cell + gap); y = y0 + r * (cell + gap)
        if i < filled:
            d.rectangle([x, y, x + cell, y + cell], fill=A(tuple(int(v * .45) for v in col), a), outline=A(col, a), width=2)

def sc1(L, d, t):
    a = win(t, 0, 6.45)
    if not a: return
    label(d, "01  ·  MÊME BUDGET", "PRIX MÉDIAN AU M²  /  DVF 2021-2025", a)
    # gros chiffre présent dès l'image 1
    s = 1 + 0.04 * math.sin(min(t, 1.4) * 2.2)
    d.text((MX, 300), "Avec", font=SERIF(64), fill=A(DIM, a))
    d.text((MX, 370), "200 000 €,", font=SERIF_I(int(150 * s)), fill=A(GOLD, a))
    d.text((MX, 560), "tu achètes combien de m² ?", font=SERIF(58), fill=A(TXT, a))
    # deux colonnes
    yb = 720
    for k, (city, price, m2, t0, col) in enumerate([("PARIS", "10 241 €/m²", 20, 1.7, RED), ("GRENOBLE", "2 595 €/m²", 77, 4.2, GREEN)]):
        x0 = MX if k == 0 else 570
        d.text((x0, yb), city, font=COND(52), fill=A(TXT, a))
        d.text((x0, yb + 72), price, font=MONO(22), fill=A(DIM, a))
        prog = eio((t - t0) / (1.6 if k == 0 else 1.4))
        filled = int(round(m2 * prog))
        floor(d, x0, yb + 130, 10, 80, filled, col, a, cell=34, gap=5)
        if prog > 0:
            d.text((x0, yb + 130 + 8 * 39 + 30), f"{filled} m²", font=SERIF(84), fill=A(col if prog >= 1 else TXT, a))
    d.text((MX, 1310), "1 carré = 1 m²", font=MONO(19), fill=A(DIM2, a))

# ---- Scène 2 : loyers ----
def sc2(L, d, t):
    a = win(t, 6.55, 11.5)
    if not a: return
    label(d, "02  ·  LE LOYER", "LOYER MÉDIAN AU M²  /  PARIS 33,3 €  ·  GRENOBLE 12,4 €", a)
    d.text((MX, 300), "Et le loyer ?", font=SERIF(84), fill=A(TXT, a))
    rows = [("PARIS", 650, 7.75, RED, "20 m²"), ("GRENOBLE", 953, 9.9, GREEN, "77 m²")]
    for i, (city, rent, t0, col, sz) in enumerate(rows):
        y = 560 + i * 330
        p = eio((t - t0) / 1.3)
        d.text((MX, y), city, font=COND(48), fill=A(TXT, a))
        d.text((MX + 260, y + 18), sz, font=MONO(22), fill=A(DIM, a))
        n = int(round(rent / 50 * p))
        for j in range(n):
            r, c = divmod(j, 10)
            bill(L, MX + c * 86, y + 90 + r * 50, 76, 40, col, a)
        if p > 0:
            d.text((W - MX, y), f"{eur(rent * p)}/mois", font=SERIF(60), fill=A(col if p >= 1 else TXT, a), anchor="ra")
    d.text((MX, 1300), "1 billet = 50 €", font=MONO(19), fill=A(DIM2, a))

# ---- Scène 3 : écart annuel ----
def sc3(L, d, t):
    a = win(t, 11.6, 16.75)
    if not a: return
    label(d, "03  ·  L'ÉCART", "RENDEMENT BRUT  /  PARIS 3,9 %  ·  GRENOBLE 5,7 %", a)
    p = eio((t - 11.7) / 2.4)
    v = 3626 * p
    sc = back((t - 11.7) / 0.5)
    d.text((W / 2, 640), "+ " + eur(v), font=SERIF_I(int(170 * max(.4, sc))), fill=A(GOLD, a), anchor="mm")
    d.text((W / 2, 790), "de loyers en plus, chaque année", font=SERIF(54), fill=A(TXT, a), anchor="mm")
    if t > 15.1:
        q = a * eo((t - 15.1) / 0.4)
        d.rectangle([MX + 120, 900, W - MX - 120, 990], fill=A(CHIP, q), outline=A(GOLD, q), width=2)
        d.text((W / 2, 945), "pour la même somme investie", font=MONO(28), fill=A(GOLD, q), anchor="mm")
    # rendements en pastilles
    chip(d, MX, 1060, 410, 150, "PARIS", "3,9 % brut", RED, a)
    chip(d, W - MX - 410, 1060, 410, 150, "GRENOBLE", "5,7 % brut", GREEN, a)

# ---- Scène 4 : la leçon ----
def sc4(L, d, t):
    a = win(t, 16.85, 20.05)
    if not a: return
    label(d, "04  ·  LA LEÇON", "", a)
    d.text((MX, 520), "Investir là où", font=SERIF(96), fill=A(TXT, a))
    d.text((MX, 640), "tu habites…", font=SERIF(96), fill=A(TXT, a))
    q = eo((t - 18.2) / 0.5)
    d.text((MX, 800), "c'est souvent le", font=SERIF(96), fill=A(DIM, a * q))
    d.text((MX, 920), "choix le plus cher.", font=SERIF_I(104), fill=A(RED, a * q))

# ---- Scène 5 : CTA ----
def sc5(L, d, t):
    a = win(t, 20.1, 23.61, fout=0.5)
    if not a: return
    label(d, "05  ·  NEWSLETTER GRATUITE", "UN CALCUL PAR SEMAINE", a)
    d.text((MX, 400), "Tu veux la carte", font=SERIF(84), fill=A(TXT, a))
    d.text((MX, 505), "des rendements ?", font=SERIF_I(90), fill=A(GOLD, a))
    x0, y0, x1, y1 = MX, 760, W - MX, 890
    d.rectangle([x0, y0, x1, y1], fill=A(CHIP, a), outline=A(CHIPB, a), width=2)
    d.text((x0 + 24, y0 + 16), "COMMENTAIRE", font=MONO(17), fill=A(DIM, a))
    typed = "VILLE"[:int(cl((t - 20.4) / 0.8) * 5)]
    cur = "|" if int(t * 2.5) % 2 == 0 else " "
    d.text((x0 + 24, y0 + 46), typed + cur, font=SERIF(58), fill=A(GOLD, a))
    d.text((x1 - 24, (y0 + y1) / 2 + 8), "PUBLIER", font=MONO(22), fill=A(TXT if typed == "VILLE" else DIM, a), anchor="rm")
    bob = math.sin(t * 5) * 10
    d.polygon([(W / 2 - 22, 970 + bob), (W / 2 + 22, 970 + bob), (W / 2, 1002 + bob)], fill=A(DIM, a))

def end_card(L, d, t):
    if t < 23.66: return
    a = eo((t - 23.66) / 0.5)
    d.text((W / 2, 880), "Commente VILLE", font=SERIF_I(80), fill=A(GOLD, a), anchor="mm")
    d.text((W / 2, 970), "pour recevoir la newsletter", font=SERIF(44), fill=A(TXT, a), anchor="mm")
    for i, line in enumerate(["Contenu éducatif, pas un conseil personnalisé.",
                              "Rendements bruts médians 2021-2025, hors charges et fiscalité.",
                              "Source : Meilleurtaux / Lokimo (DVF), fév. 2026."]):
        d.text((W / 2, 1580 + i * 34), line, font=MONO(18), fill=A(DIM2, a), anchor="mm")

def captions(L, d, t):
    if t > AUDIO + 0.2: return
    cur = None
    for i, (s, e, _) in enumerate(SEGS):
        if t >= s - 0.05: cur = i
    if cur is None: return
    s, e, _ = SEGS[cur]
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

SCENES = [sc1, sc2, sc3, sc4, sc5, end_card]
STARTS = [0, 6.55, 11.6, 16.85, 20.1, 23.66]
def frame(t):
    to = tmap(t)
    img = BG.copy(); L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for sc in SCENES: sc(L, d, to)
    if THEME == "b":
        st = max(x for x in STARTS if x <= to)
        k = to - st
        z = 1 + 0.07 * (1 - eo(k / 0.45)) + 0.012 * min(k, 5) / 5
        if abs(z - 1) > 1e-3:
            Z = L.resize((int(W * z), int(H * z)), Image.BILINEAR)
            L = Z.crop((int((Z.width - W) / 2), int((Z.height - H) / 2), int((Z.width - W) / 2) + W, int((Z.height - H) / 2) + H))
    C = Image.new("RGBA", (W, H), (0, 0, 0, 0)); captions(C, ImageDraw.Draw(C), t)
    img.alpha_composite(L); img.alpha_composite(C); return img.convert("RGB")

if __name__ == "__main__":
    if sys.argv[1:2] == ["stills"]:
        ims = [frame(float(x)) for x in sys.argv[2:]]
        sh = Image.new("RGB", (270 * len(ims), 480))
        for i, im in enumerate(ims): sh.paste(im.resize((270, 480)), (270 * i, 0))
        sh.save("contact.png"); sys.exit()
    out = sys.argv[1]
    n = int(DUR * FPS)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-i", {"vic": "voix_vic.mp3", "fl": "voix_fl.mp3"}[VOICE], "-filter_complex", f"[1:a]apad=pad_dur={TAIL}[a]",
                          "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                          "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", str(DUR), "-movflags", "+faststart", out],
                         stdin=subprocess.PIPE)
    for i in range(n): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print("ok", n)
