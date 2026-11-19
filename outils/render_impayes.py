"""NOIR format B : loyers impayés / GLI."""
import math, subprocess, sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

THEME = "b"
W, H, FPS = 1080, 1920, 30
AUDIO = 36.05
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


# ---- 1 : hook ----
def sc1(L, d, t):
    a = win(t, 0, 3.3)
    if not a: return
    label(d, "01  ·  LOYERS IMPAYÉS", "CE QUE ÇA COÛTE VRAIMENT", a)
    d.text((MX, 330), "Ton locataire", font=SERIF(104), fill=A(TXT, a))
    d.text((MX, 455), "arrête de payer…", font=SERIF_I(112), fill=A(GOLD, a))
    sc = 1 if t < 2.0 else 1 + 0.06 * math.sin((t - 2.0) * 9) * max(0, 1 - (t - 2.0) / 1.0)
    d.text((MX, 680), "tu perds", font=SERIF(96), fill=A(TXT, a))
    d.text((MX, 800), "combien ?", font=SERIF_I(int(140 * sc)), fill=A(RED, a))
    # boîte aux lettres vide qui tremble
    sh = math.sin(t * 22) * 6 if t > 1.0 else 0
    cx, cy = 790 + sh, 1150
    d.rounded_rectangle([cx - 150, cy - 90, cx + 150, cy + 90], 22, fill=A(CHIP, a), outline=A(RED, a), width=4)
    d.text((cx, cy - 10), "0 €", font=SERIF_I(88), fill=A(RED, a), anchor="mm")
    d.text((cx, cy + 58), "LOYER REÇU", font=MONO(18), fill=A(DIM, a), anchor="mm")

# ---- 2 : loyer + durée procédure ----
def sc2(L, d, t):
    a = win(t, 3.4, 10.6)
    if not a: return
    label(d, "02  ·  EXEMPLE ILLUSTRATIF", "LOYER 900 € / MOIS CHARGES COMPRISES", a)
    q = eo((t - 3.5) / .4)
    d.text((MX, 320), "900 €", font=SERIF_I(int(130 * max(.5, back((t - 5.1) / .5)))), fill=A(GOLD, a * q))
    d.text((MX + 420, 370), "par mois", font=SERIF(60), fill=A(TXT, a * q))
    if t > 7.1:
        q2 = eo((t - 7.1) / .4)
        d.text((MX, 560), "Procédure d'expulsion", font=SERIF(72), fill=A(TXT, a * q2))
        d.text((MX, 650), "en moyenne", font=MONO(26), fill=A(DIM, a * q2))
        x0, x1, y = MX, W - MX, 820
        d.rectangle([x0, y, x1, y + 70], fill=A(CHIP, a * q2), outline=A(CHIPB, a * q2), width=2)
        n = 12; cw = (x1 - x0) / n
        p = cl((t - 7.6) / 2.4)
        for i in range(n):
            if i / n < p:
                col = GOLD if i < 8 else RED
                d.rectangle([x0 + i * cw + 4, y + 6, x0 + (i + 1) * cw - 4, y + 64], fill=A(tuple(int(c * .6) for c in col), a))
        for m, col in [(8, GOLD), (12, RED)]:
            if p >= m / n - 1e-6:
                xx = x0 + m * cw
                d.text((min(xx, x1), y + 120), f"{m} mois", font=SERIF_I(58), fill=A(col, a), anchor="rm" if m == 12 else "mm")

# ---- 3 : trêve hivernale ----
MOIS = ["S", "O", "N", "D", "J", "F", "M", "A", "M", "J"]
def sc3(L, d, t):
    a = win(t, 10.7, 15.5)
    if not a: return
    label(d, "03  ·  TRÊVE HIVERNALE", "PAS D'EXPULSION DU 1ER NOVEMBRE AU 31 MARS", a)
    d.text((MX, 320), "Et l'hiver", font=SERIF(96), fill=A(TXT, a))
    d.text((MX, 440), "repousse tout.", font=SERIF_I(104), fill=A(BLUE, a))
    y = 700; cw = (W - 2 * MX) / len(MOIS)
    for i, m in enumerate(MOIS):
        p = back((t - 10.9 - i * 0.08) / .5)
        if p <= 0: continue
        win_ = 2 <= i <= 6
        x = MX + i * cw
        hh = 230 * min(1.1, p)
        col = BLUE if (win_ and t > 11.6) else DIM2
        d.rectangle([x + 6, y + 230 - hh, x + cw - 6, y + 230], fill=A(tuple(int(c * .45) for c in col), a), outline=A(col, a), width=3)
        d.text((x + cw / 2, y + 280), m, font=COND(44), fill=A(TXT if win_ else DIM, a), anchor="mm")
    if t > 12.0:
        q = eo((t - 12.0) / .4)
        d.text((MX + 2 * cw + 2.5 * cw, y - 50), "1er nov  →  31 mars", font=MONO(28), fill=A(BLUE, a * q), anchor="mm")
    # flocons
    for i in range(14):
        fx = MX + (i * 73) % (W - 2 * MX)
        fy = 1080 + ((t * 60 + i * 37) % 200)
        d.text((fx, fy), "*", font=MONO(40), fill=A(BLUE, a * .6))

# ---- 4 : perte ----
def sc4(L, d, t):
    a = win(t, 15.6, 20.9)
    if not a: return
    label(d, "04  ·  LA PERTE", "12 MOIS × 900 €", a)
    d.text((MX, 320), "12 mois sans loyer", font=SERIF(80), fill=A(TXT, a))
    p = eo((t - 17.1) / 1.0)
    v = 10800 * p
    sc = max(.5, back((t - 17.1) / .5))
    d.text((MX, 440), "−" + eur(v), font=SERIF_I(int(130 * sc)), fill=A(RED, a))
    # billets qui s'envolent
    for i in range(12):
        tt = t - 15.8 - i * 0.12
        if tt <= 0: continue
        x = MX + 40 + (i % 6) * 140 + math.sin(tt * 3 + i) * 20
        y = 1120 - (i // 6) * 120 - tt * 90
        al = a * cl(1 - (tt - 2.5) / 1.0)
        if al > 0: bill(L, x, y, 120, 62, RED, al, rot=int(math.sin(tt * 2 + i) * 14))
    if t > 18.9:
        q = eo((t - 18.9) / .4)
        chip(d, MX, 1200, W - 2 * MX, 150, "ET PENDANT CE TEMPS", "ton crédit continue", TXT, a * q, vsize=56)
        k = int((t - 18.9) * 3)
        for j in range(min(k, 6)):
            d.ellipse([W - MX - 60 - j * 46, 1240, W - MX - 30 - j * 46, 1270], fill=A(RED, a * q))

# ---- 5 : GLI ----
def sc5(L, d, t):
    a = win(t, 21.0, 29.9)
    if not a: return
    label(d, "05  ·  LA PARADE", "GARANTIE LOYERS IMPAYÉS (GLI)", a)
    q = eo((t - 21.1) / .4)
    d.text((MX, 320), "Garantie", font=SERIF(96), fill=A(TXT, a * q))
    d.text((MX, 430), "loyers impayés", font=SERIF_I(100), fill=A(LIME, a * q))
    # bouclier
    bob = math.sin(t * 3) * 10
    cx, cy = W / 2, 820 + bob
    pb = back((t - 21.4) / .6)
    s = 170 * max(0, pb)
    if s > 1:
        d.polygon([(cx - s, cy - s * .8), (cx + s, cy - s * .8), (cx + s, cy + s * .1), (cx, cy + s * 1.05), (cx - s, cy + s * .1)],
                  fill=A((20, 34, 22), a), outline=A(LIME, a), width=5)
        if t > 23.0:
            d.text((cx, cy - 10), "2,5 à 5 %", font=SERIF_I(int(70 * max(.5, back((t - 23.0) / .5)))), fill=A(LIME, a), anchor="mm")
            d.text((cx, cy + 62), "DU LOYER ANNUEL", font=MONO(20), fill=A(DIM, a), anchor="mm")
    if t > 26.0:
        q2 = eo((t - 26.0) / .4)
        chip(d, MX, 1080, 420, 150, "ICI, PAR MOIS", "30 € environ", GOLD, a * q2, vsize=52)
    if t > 27.8:
        q3 = eo((t - 27.8) / .4)
        chip(d, MX + 460, 1080, W - 2 * MX - 460, 150, "FISCALITÉ", "déductible au réel", TXT, a * q3, vsize=44)

# ---- 6 : CTA ----
def sc6(L, d, t):
    a = win(t, 30.0, 35.75, fout=0.5)
    if not a: return
    label(d, "06  ·  NEWSLETTER GRATUITE", "UN CALCUL PAR SEMAINE", a)
    d.text((MX, 400), "Tu loues", font=SERIF(84), fill=A(TXT, a))
    d.text((MX, 505), "sans filet ?", font=SERIF_I(96), fill=A(GOLD, a))
    x0, y0, x1, y1 = MX, 760, W - MX, 890
    d.rectangle([x0, y0, x1, y1], fill=A(CHIP, a), outline=A(CHIPB, a), width=2)
    d.text((x0 + 24, y0 + 16), "COMMENTAIRE", font=MONO(17), fill=A(DIM, a))
    word = "GARANTIE"
    typed = word[:int(cl((t - 32.6) / 0.9) * len(word))]
    cur = "|" if int(t * 2.5) % 2 == 0 else " "
    d.text((x0 + 24, y0 + 46), typed + cur, font=SERIF(58), fill=A(GOLD, a))
    d.text((x1 - 24, (y0 + y1) / 2 + 8), "PUBLIER", font=MONO(22), fill=A(TXT if typed == word else DIM, a), anchor="rm")
    bob = math.sin(t * 5) * 10
    d.polygon([(W / 2 - 22, 970 + bob), (W / 2 + 22, 970 + bob), (W / 2, 1002 + bob)], fill=A(DIM, a))

def end_card(L, d, t):
    if t < 35.8: return
    a = eo((t - 35.8) / 0.5)
    d.text((W / 2, 880), "Commente GARANTIE", font=SERIF_I(80), fill=A(GOLD, a), anchor="mm")
    d.text((W / 2, 970), "pour recevoir la newsletter", font=SERIF(44), fill=A(TXT, a), anchor="mm")
    for i, line in enumerate(["Contenu éducatif, pas un conseil personnalisé.",
                              "Exemple illustratif. Durées et tarifs variables.",
                              "Sources : France Épargne, service-public.fr (2026)."]):
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
            if ws <= t < we + 0.05:
                tw = d.textlength(w, font=f)
                d.rounded_rectangle([x - 8, y - 2, x + tw + 8, y + 64], 10, fill=(198, 240, 107, 255))
                d.text((x, y), w, font=f, fill=(12, 12, 12))
            else:
                d.text((x, y), w, font=f, fill=TXT if t >= ws else (96, 94, 90))
            x += d.textlength(w + " ", font=f)
        y += 64

SCENES = [sc1, sc2, sc3, sc4, sc5, sc6, end_card]
STARTS = [0, 3.4, 10.7, 15.6, 21.0, 30.0, 35.8]
def frame(t):
    img = BG.copy(); L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for sc in SCENES: sc(L, d, t)
    st = max(x for x in STARTS if x <= t)
    k = t - st
    z = 1 + (0.07 * (1 - eo(k / 0.45)) if st > 0 else 0) + 0.012 * min(k, 5) / 5
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
