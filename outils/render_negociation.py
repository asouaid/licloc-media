"""NOIR format A (Victoria, THEME a) : négocier le prix, 4,8 % = ~14 700 € gagnés."""
import math, subprocess, sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

THEME = "a"
W, H, FPS = 1080, 1920, 30
AUDIO = 31.1
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



def tag(d, cx, cy, txt, a, col, s=1.0, strike=0):
    f = SERIF_I(int(130 * s)); tw = d.textlength(txt, font=f)
    x0, x1, y0, y1 = cx - tw / 2 - 60, cx + tw / 2 + 40, cy - 95 * s, cy + 95 * s
    d.polygon([(x0, cy), (x0 + 50 * s, y0), (x1, y0), (x1, y1), (x0 + 50 * s, y1)], fill=A(CHIP, a), outline=A(col, a))
    d.ellipse([x0 + 40 * s, cy - 12 * s, x0 + 64 * s, cy + 12 * s], outline=A(DIM, a), width=3)
    d.text((cx + 20, cy), txt, font=f, fill=A(col, a), anchor="mm")
    if strike > 0:
        d.line([x0 + 70 * s, cy, x0 + 70 * s + (x1 - x0 - 90 * s) * strike, cy], fill=A(RED, a), width=10)

# ---- 1 : hook ----
def sc1(L, d, t):
    a = win(t, 0, 3.55)
    if not a: return
    label(d, "01  ·  NÉGOCIATION", "LE PRIX AFFICHÉ, TU LE PAIES ?", a)
    sc = max(.6, back(t / .5)) if t > 0 else 1
    d.text((MX, 330), "Ton appart", font=SERIF(88), fill=A(TXT, a))
    tag(d, W / 2, 640, "200 000 €", a, GOLD, sc, strike=eo((t - 2.2) / .6) if t > 2.2 else 0)
    d.text((MX, 860), "tu le paies", font=SERIF(88), fill=A(TXT, a))
    d.text((MX, 970), "vraiment ?", font=SERIF_I(110), fill=A(GOLD, a))
    for i in range(5):
        bill(L, 620 + i * 30, 1180 - i * 20 + math.sin(t * 3 + i) * 6, 260, 100, GOLD, a, rot=int(6 * math.sin(i + 1)))

# ---- 2 : marge moyenne ----
def sc2(L, d, t):
    a = win(t, 3.65, 9.35)
    if not a: return
    label(d, "02  ·  MARGE DE NÉGOCIATION MOYENNE", "ANCIEN · SEPTEMBRE 2026 · LAFORÊT", a)
    v = 4.8 * eo((t - 3.8) / 1.2)
    d.text((MX, 300), f"{v:.1f} %".replace(".", ","), font=SERIF_I(int(190 * max(.6, back((t - 3.8) / .5)))), fill=A(GOLD, a))
    d.text((MX, 530), "en moyenne en France", font=SERIF(56), fill=A(DIM, a))
    base = 1300; mh = 520; w = 230
    for k, (lab, val, t0) in enumerate([("PARIS", 3.2, 5.6), ("ÎLE-DE-FR.", 4.6, 6.2), ("RÉGIONS", 5.1, 6.8)]):
        x0 = MX + 20 + k * 300
        p = back((t - t0) / .7) if t > t0 else 0
        h = mh * val / 5.1 * p
        col = GOLD if k == 2 else TXT
        if h > 0:
            d.rectangle([x0, base - h, x0 + w, base], fill=A(tuple(int(c * .3) for c in col), a), outline=A(col, a), width=3)
            if p >= .9: d.text((x0 + w / 2, base - h - 50), f"{val} %".replace(".", ","), font=SERIF(54), fill=A(col, a), anchor="mm")
        d.text((x0 + w / 2, base + 42), lab, font=COND(36), fill=A(TXT, a), anchor="mm")

# ---- 3 : sur 200 000 ----
def sc3(L, d, t):
    a = win(t, 9.45, 13.7)
    if not a: return
    label(d, "03  ·  EXEMPLE ILLUSTRATIF", "PRIX AFFICHÉ 200 000 €  ·  − 4,8 %", a)
    q = eo((t - 9.5) / .4)
    p = eio((t - 10.4) / 1.4)
    tag(d, W / 2, 470, eur(200000 - 9600 * p), a * q, TXT if p < 1 else GOLD, 1.0)
    if t > 11.0:
        s2 = max(.5, back((t - 11.0) / .5))
        d.text((W / 2, 800), "− 9 600 €", font=SERIF_I(int(150 * s2)), fill=A(GREEN, a), anchor="mm")
        d.text((W / 2, 930), "sur le prix", font=MONO(28), fill=A(DIM, a), anchor="mm")
    for i in range(6):
        tt = t - 11.2 - i * .12
        if tt > 0: bill(L, 160 + i * 130, 1060 + 40 * math.sin(i) - tt * 60, 170, 80, GREEN, a * cl(tt / .3), rot=int(10 * math.sin(i * 2)))

# ---- 4 : frais de notaire ----
def sc4(L, d, t):
    a = win(t, 13.8, 18.3)
    if not a: return
    label(d, "04  ·  FRAIS DE NOTAIRE", "ENVIRON 8 % DU PRIX DANS L'ANCIEN", a)
    q = eo((t - 13.9) / .4)
    d.text((MX, 320), "Calculés", font=SERIF(88), fill=A(TXT, a * q))
    d.text((MX, 430), "sur le prix", font=SERIF_I(100), fill=A(GOLD, a * q))
    if t > 15.4:
        p = eo((t - 15.4) / .5)
        chip(d, MX, 660, W - 2 * MX, 160, "8 % × 9 600 €", "", TXT, a * p)
        v = 768 * eo((t - 15.6) / 1.0)
        d.text((MX + 22, 706), f"{int(round(v))} €", font=SERIF_I(70), fill=A(TXT, a * p))
    if t > 16.6:
        s2 = max(.5, back((t - 16.6) / .5))
        d.text((W / 2, 1060), "− 770 €", font=SERIF_I(int(150 * s2)), fill=A(GREEN, a), anchor="mm")
        d.text((W / 2, 1190), "de frais en moins", font=MONO(28), fill=A(DIM, a), anchor="mm")

# ---- 5 : intérêts ----
def sc5(L, d, t):
    a = win(t, 18.4, 24.1)
    if not a: return
    label(d, "05  ·  LE CRÉDIT", "20 ANS · 3,7 % · TAUX MOYEN NOV. 2026 (MEILLEURTAUX)", a)
    q = eo((t - 18.5) / .4)
    chip(d, MX, 310, 420, 170, "EMPRUNT EN MOINS", "10 370 €", GOLD, a * q, vsize=62)
    if t > 19.4:
        q2 = eo((t - 19.4) / .4)
        chip(d, MX + 460, 310, W - 2 * MX - 460, 170, "DURÉE · TAUX", "20 ans · 3,7 %", TXT, a * q2, vsize=54)
    # 20 années qui défilent
    n = int(cl((t - 20.0) / 2.0) * 20)
    for i in range(20):
        x = MX + (i % 10) * 88; y = 600 + (i // 10) * 110
        on = i < n
        d.rectangle([x, y, x + 70, y + 80], fill=A(tuple(int(c * .35) for c in RED) if on else CHIP, a), outline=A(RED if on else CHIPB, a), width=2)
        d.text((x + 35, y + 40), str(i + 1), font=MONO(22), fill=A(TXT if on else DIM2, a), anchor="mm")
    if t > 21.8:
        v = 4320 * eo((t - 21.8) / 1.0)
        s2 = max(.5, back((t - 21.8) / .5))
        d.text((W / 2, 1000), "− " + eur(round(v, -1) if v < 4320 else 4300), font=SERIF_I(int(140 * s2)), fill=A(GREEN, a), anchor="mm")
        d.text((W / 2, 1125), "d'intérêts évités (environ)", font=MONO(28), fill=A(DIM, a), anchor="mm")

# ---- 6 : total ----
def sc6(L, d, t):
    a = win(t, 24.2, 28.5)
    if not a: return
    label(d, "06  ·  AU TOTAL", "EXEMPLE ILLUSTRATIF", a)
    q = eo((t - 24.3) / .4)
    d.text((MX, 310), "près de", font=SERIF(80), fill=A(TXT, a * q))
    v = 14700 * eo((t - 24.5) / 1.4)
    d.text((MX, 410), eur(round(v, -2)), font=SERIF_I(170), fill=A(GOLD, a * q))
    base = 1330; tot = 14690; mh = 600; x0 = W / 2 - 170; w = 340; y = base
    for k, (lab, val, col, t0) in enumerate([("PRIX", 9600, GREEN, 24.6), ("NOTAIRE", 770, BLUE, 25.2), ("INTÉRÊTS", 4320, GOLD, 25.6)]):
        p = eo((t - t0) / .6) if t > t0 else 0
        h = mh * val / tot * p
        if h > 0:
            d.rectangle([x0, y - h, x0 + w, y], fill=A(tuple(int(c * .35) for c in col), a), outline=A(col, a), width=3)
            if p > .9:
                d.text((x0 + w + 30, y - h / 2), lab, font=COND(34), fill=A(col, a), anchor="lm")
                d.text((x0 - 30, y - h / 2), eur(val if val != 4320 else 4300), font=MONO(26), fill=A(TXT, a), anchor="rm")
        y -= h
    if t > 26.8:
        d.text((W / 2, 1390), "pour une offre bien argumentée", font=SERIF_I(48), fill=A(TXT, a * eo((t - 26.8) / .4)), anchor="mm")

# ---- 7 : CTA ----
def sc7(L, d, t):
    a = win(t, 28.6, 31.05, fout=0.5)
    if not a: return
    label(d, "07  ·  NEWSLETTER GRATUITE", "UN CALCUL PAR SEMAINE", a)
    d.text((MX, 400), "Tu veux d'autres", font=SERIF(84), fill=A(TXT, a))
    d.text((MX, 505), "calculs comme ça ?", font=SERIF_I(90), fill=A(GOLD, a))
    x0, y0, x1, y1 = MX, 760, W - MX, 890
    d.rectangle([x0, y0, x1, y1], fill=A(CHIP, a), outline=A(CHIPB, a), width=2)
    d.text((x0 + 24, y0 + 16), "COMMENTAIRE", font=MONO(17), fill=A(DIM, a))
    word = "OFFRE"
    typed = word[:int(cl((t - 29.9) / 0.6) * len(word))]
    cur = "|" if int(t * 2.5) % 2 == 0 else " "
    d.text((x0 + 24, y0 + 46), typed + cur, font=SERIF(58), fill=A(GOLD, a))
    d.text((x1 - 24, (y0 + y1) / 2 + 8), "PUBLIER", font=MONO(22), fill=A(TXT if typed == word else DIM, a), anchor="rm")
    bob = math.sin(t * 5) * 10
    d.polygon([(W / 2 - 22, 970 + bob), (W / 2 + 22, 970 + bob), (W / 2, 1002 + bob)], fill=A(DIM, a))

def end_card(L, d, t):
    if t < 31.1: return
    a = eo((t - 31.1) / 0.5)
    d.text((W / 2, 880), "Commente OFFRE", font=SERIF_I(80), fill=A(GOLD, a), anchor="mm")
    d.text((W / 2, 970), "pour recevoir la newsletter", font=SERIF(44), fill=A(TXT, a), anchor="mm")
    for i, line in enumerate(["Contenu éducatif, pas un conseil personnalisé. Exemple illustratif.",
                              "Marge de négociation : Laforêt, 3e trimestre 2026 (septembre).",
                              "Taux : Meilleurtaux, novembre 2026. Frais de notaire : environ 8 % (ancien)."]):
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

SCENES = [sc1, sc2, sc3, sc4, sc5, sc6, sc7, end_card]
STARTS = [0, 3.65, 9.45, 13.8, 18.4, 24.2, 28.6, 31.1]
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
