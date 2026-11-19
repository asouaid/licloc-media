"""NOIR format A (Victoria, THEME a) : effet de levier du crédit."""
import math, subprocess, sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

THEME = "a"
W, H, FPS = 1080, 1920, 30
AUDIO = 36.6
TAIL = 2.0
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
    gd.ellipse([W / 2 - 520, 520, W / 2 + 520, 1500], fill=(34, 28, 16))
    g = np.asarray(g.filter(ImageFilter.GaussianBlur(160)), dtype="int16")
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


# ---- 1 : hook ----
def sc1(L, d, t):
    a = win(t, 0, 3.9)
    if not a: return
    label(d, "01  ·  EFFET DE LEVIER", "CASH OU CRÉDIT ?", a)
    sc = max(.5, back(t / .5)) if t > 0 else 1
    d.text((MX, 320), "200 000 €", font=SERIF_I(int(150 * sc)), fill=A(GOLD, a))
    d.text((MX, 500), "en poche…", font=SERIF(96), fill=A(TXT, a))
    q = eo((t - 2.0) / .35) if t > 0 else 1
    for k, (lab, col, x) in enumerate([("cash", TXT, MX), ("crédit ?", GOLD, MX + 450)]):
        on = (int(t * 2.2) % 2 == k) and t > 2.0
        y = 760 - (18 if on else 0)
        d.rectangle([x, y, x + 400, y + 170], fill=A(CHIP, a * q), outline=A(GOLD if on else CHIPB, a * q), width=3)
        d.text((x + 200, y + 85), lab, font=SERIF_I(80), fill=A(col, a * q), anchor="mm")
    d.text((W / 2, 1040), "ou", font=MONO(26), fill=A(DIM, a * q), anchor="mm")
    # pile de billets
    for i in range(7):
        bill(L, 380 + (i % 2) * 14, 1150 - i * 22, 320, 120, GOLD, a)

# ---- 2 : exemple ----
def house(d, cx, cy, s, a, col):
    d.polygon([(cx - s, cy), (cx, cy - s * .8), (cx + s, cy)], fill=A(tuple(int(c * .5) for c in col), a), outline=A(col, a))
    d.rectangle([cx - s * .8, cy, cx + s * .8, cy + s * 1.1], fill=A(CHIP, a), outline=A(col, a), width=3)
    d.rectangle([cx - s * .18, cy + s * .55, cx + s * .18, cy + s * 1.1], fill=A(col, a * .7))

def sc2(L, d, t):
    a = win(t, 4.0, 11.9)
    if not a: return
    label(d, "02  ·  EXEMPLE ILLUSTRATIF", "BIEN À 200 000 €  ·  RENDEMENT BRUT 5 %", a)
    p = back((t - 4.2) / .6)
    if p > 0: house(d, 300, 520, 170 * p, a, GOLD)
    if t > 5.8:
        q = eo((t - 5.8) / .4)
        d.text((560, 380), "5 %", font=SERIF_I(int(130 * max(.5, back((t - 5.8) / .5)))), fill=A(GOLD, a * q))
        d.text((560, 540), "par an", font=MONO(26), fill=A(DIM, a * q))
    if t > 7.4:
        v = 10000 * eo((t - 7.4) / .9)
        d.text((MX, 820), eur(v), font=SERIF(104), fill=A(TXT, a))
        d.text((MX, 950), "de loyers par an", font=SERIF_I(60), fill=A(DIM, a))
        for i in range(5):
            tt = t - 7.6 - i * .15
            if tt > 0: bill(L, 640 + i * 50, 840 + math.sin(tt * 4 + i) * 10, 150, 78, GREEN, a * cl(tt / .3), rot=int(8 * math.sin(i)))
    if t > 9.9:
        q = eo((t - 9.9) / .4)
        chip(d, MX, 1120, W - 2 * MX, 160, "PAYÉ CASH  ·  200 000 € INVESTIS", "5 % par an", GOLD, a * q, vsize=64, vfont=SERIF_I)

# ---- 3 : crédit ----
def sc3(L, d, t):
    a = win(t, 12.0, 19.5)
    if not a: return
    label(d, "03  ·  AVEC UN CRÉDIT", "TAUX MOYEN 20 ANS, NOV. 2026 (MEILLEURTAUX)", a)
    q = eo((t - 12.1) / .4)
    chip(d, MX, 310, 420, 170, "APPORT", "20 000 €", GOLD, a * q, vsize=66)
    if t > 13.6:
        q2 = eo((t - 13.6) / .4)
        chip(d, MX + 460, 310, W - 2 * MX - 460, 170, "CRÉDIT 180 000 €", "3,7 % · 20 ans", TXT, a * q2, vsize=54)
    base = 1250; mh = 560; w = 300
    for k, (lab, v, t0, col) in enumerate([("LOYERS", 10000, 14.2, GREEN), ("INTÉRÊTS AN 1", 6556, 16.6, RED)]):
        x0 = MX + 60 + k * 470
        p = back((t - t0) / .8) if t > t0 else 0
        h = mh * v / 10000 * p
        if h > 0:
            d.rectangle([x0, base - h, x0 + w, base], fill=A(tuple(int(c * .35) for c in col), a), outline=A(col, a), width=3)
            vv = "−6 500 €" if k else "10 000 €"
            if p >= .9: d.text((x0 + w / 2, base - h - 56), vv, font=SERIF(56), fill=A(col, a), anchor="mm")
        d.text((x0 + w / 2, base + 46), lab, font=COND(40), fill=A(TXT, a), anchor="mm")

# ---- 4 : résultat ----
def sc4(L, d, t):
    a = win(t, 19.6, 25.2)
    if not a: return
    label(d, "04  ·  LE RÉSULTAT", "AVANT CHARGES ET IMPÔTS", a)
    q = eo((t - 19.8) / .4)
    d.text((MX, 320), "Il te reste", font=SERIF(84), fill=A(TXT, a * q))
    d.text((MX, 430), "3 400 €", font=SERIF_I(130), fill=A(GOLD, a * q))
    d.text((MX, 600), "pour 20 000 € investis", font=SERIF(58), fill=A(DIM, a * q))
    base = 1330; mh = 520; w = 280
    for k, (lab, v, t0, col) in enumerate([("CASH", 5, 22.0, DIM), ("CRÉDIT", 17, 22.9, GREEN)]):
        x0 = MX + 80 + k * 460
        p = back((t - t0) / .8) if t > t0 else 0
        h = mh * v / 17 * p
        if h > 0:
            d.rectangle([x0, base - h, x0 + w, base], fill=A(tuple(int(c * .35) for c in col), a), outline=A(col, a), width=3)
            if p >= .9: d.text((x0 + w / 2, base - h - 64), f"{v} %", font=SERIF_I(80 if k else 56), fill=A(col if k else TXT, a), anchor="mm")
        d.text((x0 + w / 2, base + 46), lab, font=COND(42), fill=A(TXT, a), anchor="mm")

# ---- 5 : le piège ----
def sc5(L, d, t):
    a = win(t, 25.3, 31.1)
    if not a: return
    label(d, "05  ·  LE PIÈGE", "", a)
    q = eo((t - 25.4) / .4)
    d.text((MX, 320), "Rendement 3 %", font=SERIF(84), fill=A(TXT, a * q))
    d.text((MX, 430), "taux 3,7 %", font=SERIF_I(96), fill=A(RED, a * q))
    if t > 26.6:
        v = -556 * eo((t - 26.6) / .8)
        d.text((MX, 590), f"{int(round(v))} € / an", font=SERIF_I(80), fill=A(RED, a), )
    # balance
    if t > 28.3:
        p = eio((t - 28.3) / .8); ang = 0.18 - 0.36 * p
        cx, cy = W / 2, 1000
        d.polygon([(cx - 40, cy + 260), (cx + 40, cy + 260), (cx, cy)], fill=A(CHIPB, a))
        dx, dy = math.cos(ang) * 320, math.sin(ang) * 320
        d.line([cx - dx, cy - dy, cx + dx, cy + dy], fill=A(GOLD, a), width=8)
        for sgn, lab, col in [(-1, "rendement", GREEN), (1, "taux", RED)]:
            px, py = cx + sgn * dx, cy + sgn * dy
            d.line([px, py, px, py + 90], fill=A(DIM, a), width=3)
            d.rectangle([px - 120, py + 90, px + 120, py + 160], fill=A(CHIP, a), outline=A(col, a), width=3)
            d.text((px, py + 125), lab, font=MONO(24), fill=A(col, a), anchor="mm")
        if p >= 1: d.text((W / 2, 1340), "rendement  >  taux", font=SERIF_I(70), fill=A(GOLD, a), anchor="mm")

# ---- 6 : CTA ----
def sc6(L, d, t):
    a = win(t, 31.2, 36.55, fout=0.5)
    if not a: return
    label(d, "06  ·  NEWSLETTER GRATUITE", "UN CALCUL PAR SEMAINE", a)
    d.text((MX, 400), "Tu veux d'autres", font=SERIF(84), fill=A(TXT, a))
    d.text((MX, 505), "calculs comme ça ?", font=SERIF_I(90), fill=A(GOLD, a))
    x0, y0, x1, y1 = MX, 760, W - MX, 890
    d.rectangle([x0, y0, x1, y1], fill=A(CHIP, a), outline=A(CHIPB, a), width=2)
    d.text((x0 + 24, y0 + 16), "COMMENTAIRE", font=MONO(17), fill=A(DIM, a))
    word = "LEVIER"
    typed = word[:int(cl((t - 33.6) / 0.8) * len(word))]
    cur = "|" if int(t * 2.5) % 2 == 0 else " "
    d.text((x0 + 24, y0 + 46), typed + cur, font=SERIF(58), fill=A(GOLD, a))
    d.text((x1 - 24, (y0 + y1) / 2 + 8), "PUBLIER", font=MONO(22), fill=A(TXT if typed == word else DIM, a), anchor="rm")
    bob = math.sin(t * 5) * 10
    d.polygon([(W / 2 - 22, 970 + bob), (W / 2 + 22, 970 + bob), (W / 2, 1002 + bob)], fill=A(DIM, a))

def end_card(L, d, t):
    if t < 36.6: return
    a = eo((t - 36.6) / 0.5)
    d.text((W / 2, 880), "Commente LEVIER", font=SERIF_I(80), fill=A(GOLD, a), anchor="mm")
    d.text((W / 2, 970), "pour recevoir la newsletter", font=SERIF(44), fill=A(TXT, a), anchor="mm")
    for i, line in enumerate(["Contenu éducatif, pas un conseil personnalisé.",
                              "Exemple illustratif, avant charges, assurance et impôts.",
                              "Source taux : Meilleurtaux, baromètre du 9 novembre 2026."]):
        d.text((W / 2, 1580 + i * 34), line, font=MONO(18), fill=A(DIM2, a), anchor="mm")

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
            d.text((x, y), w, font=f, fill=TXT if t >= ws else (96, 94, 90))
            x += d.textlength(w + " ", font=f)
        y += 64

SCENES = [sc1, sc2, sc3, sc4, sc5, sc6, end_card]
STARTS = [0, 4.0, 12.0, 19.6, 25.3, 31.2, 36.6]
def frame(t):
    img = BG.copy(); L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for sc in SCENES: sc(L, d, t)
    st = max(x for x in STARTS if x <= t)
    k = t - st
    z = 1 + 0.012 * min(k, 5) / 5
    if abs(z - 1) > 1e-3:
        Z = L.resize((int(W * z), int(H * z)), Image.BILINEAR)
        L = Z.crop((int((Z.width - W) / 2), int((Z.height - H) / 2), int((Z.width - W) / 2) + W, int((Z.height - H) / 2) + H))
    C = Image.new("RGBA", (W, H), (0, 0, 0, 0)); captions(C, ImageDraw.Draw(C), t)
    img.alpha_composite(L); img.alpha_composite(C); return img.convert("RGB")

if __name__ == "__main__":
    if sys.argv[1:2] == ["stills"]:
        ims = [frame(float(x)) for x in sys.argv[2:]]
        sh = Image.new("RGB", (360 * len(ims), 640))
        for i, im in enumerate(ims): sh.paste(im.resize((360, 640)), (360 * i, 0))
        sh.save("contact.png"); sys.exit()
    out = sys.argv[1]
    n = int(DUR * FPS)
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-i", "voix.mp3", "-filter_complex", f"[1:a]apad=pad_dur={TAIL}[a]",
                          "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                          "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", str(DUR), "-movflags", "+faststart", out],
                         stdin=subprocess.PIPE)
    for i in range(n): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print("ok", n)
