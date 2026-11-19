"""NOIR B : vote du 17/11/2026, fin des interdictions de louer les passoires (pas encore la loi)."""
import sys; sys.path.insert(0, "/home/claude")
from noirbase import *

def check(d, x, y, s, col, a):
    d.line([x, y + s * .5, x + s * .38, y + s * .88, x + s, y + s * .1], fill=A(col, a), width=max(4, int(s / 7)), joint="curve")

DPEC = {"A": (0, 150, 70), "B": (60, 170, 70), "C": (150, 200, 60), "D": (240, 220, 40), "E": (245, 170, 40), "F": (235, 110, 40), "G": (220, 40, 40)}

def badge(d, cx, cy, r, lt, a, s=1):
    r = r * s
    d.rounded_rectangle([cx - r, cy - r, cx + r, cy + r], int(r * .25), fill=A(DPEC[lt], a))
    d.text((cx, cy + r * .04), lt, font=COND(int(r * 1.3)), fill=A((15, 15, 15), a), anchor="mm")

def sc1(L, d, t):
    a = win(t, 0, 2.6)
    if not a: return
    label(d, "01  ·  PASSOIRES THERMIQUES", "VOTE DE L'ASSEMBLÉE  ·  17 NOVEMBRE 2026", a)
    d.text((MX, 320), "Ton appart", font=SERIF(110), fill=A(TXT, a))
    d.text((MX, 445), "classé", font=SERIF(110), fill=A(TXT, a))
    s = 1 + 0.08 * math.sin(t * 7) * max(0, 1 - t / 1.4)
    badge(d, 560, 518, 82, "G", a, s)
    d.text((MX, 660), "tu peux le", font=SERIF(100), fill=A(TXT, a))
    d.text((MX, 780), "relouer ?", font=SERIF_I(150), fill=A(GOLD, a))
    # panneau À LOUER qui se balance
    ang = math.sin(t * 3.2) * 7
    p = Image.new("RGBA", (480, 300), (0, 0, 0, 0)); pd = ImageDraw.Draw(p)
    pd.line([220, 0, 120, 80], fill=A(DIM, a), width=4); pd.line([220, 0, 320, 80], fill=A(DIM, a), width=4)
    pd.rectangle([40, 80, 400, 260], fill=A(CHIP, a), outline=A(TXT, a), width=4)
    pd.text((220, 170), "À LOUER", font=COND(84), fill=A(TXT, a), anchor="mm")
    if t > 1.6:
        q = eo((t - 1.6) / .3)
        pd.text((415, 60), "?", font=SERIF_I(120), fill=A(GOLD, a * q), anchor="mm")
    p = p.rotate(ang, center=(220, 0), resample=Image.BICUBIC)
    L.alpha_composite(p, (MX + 140, 990))

def sc2(L, d, t):
    a = win(t, 2.7, 9.2)
    if not a: return
    label(d, "02  ·  LE VOTE", "AMENDEMENT N° 85  ·  PROJET DE LOI LOGEMENT  ·  1RE LECTURE", a)
    d.text((MX, 310), "Mardi soir,", font=SERIF(80), fill=A(TXT, a))
    d.text((MX, 410), "les députés ont voté", font=SERIF(72), fill=A(TXT, a))
    d.text((MX, 500), "la fin des interdictions", font=SERIF_I(72), fill=A(GOLD, a))
    # hémicycle 217 points
    cx, cy = W / 2, 1230
    votes = ["p"] * 108 + ["a"] * 7 + ["c"] * 102
    n = int(217 * eio((t - 4.0) / 3.2))
    rows = [(260, 44), (318, 54), (376, 62), (434, 57)]
    pts = []
    for R, k in rows:
        for j in range(k): pts.append((math.pi * (1 - j / (k - 1)), R))
    pts.sort(key=lambda x: -x[0])
    for i, (th, R) in enumerate(pts[:217]):
        if i >= n: break
        v = votes[i]; col = LIME if v == "p" else (DIM if v == "a" else RED)
        x = cx + R * math.cos(th); y = cy - R * math.sin(th)
        d.ellipse([x - 11, y - 11, x + 11, y + 11], fill=A(col, a))
    if t > 7.4:
        q = a * eo((t - 7.4) / .4)
        sc = max(.5, back((t - 7.4) / .5))
        d.text((cx - 40, cy - 60), "108", font=SERIF_I(int(110 * sc)), fill=A(LIME, q), anchor="rm")
        d.text((cx, cy - 60), "–", font=SERIF(90), fill=A(DIM, q), anchor="mm")
        d.text((cx + 40, cy - 60), "102", font=SERIF_I(int(110 * sc)), fill=A(RED, q), anchor="lm")
        d.text((cx, cy + 20), "POUR · CONTRE · 7 ABSTENTIONS", font=MONO(20), fill=A(DIM, q), anchor="mm")

def sc3(L, d, t):
    a = win(t, 9.3, 16.05)
    if not a: return
    label(d, "03  ·  LE CALENDRIER ACTUEL", "LOI CLIMAT ET RÉSILIENCE (2021)  ·  DÉCENCE ÉNERGÉTIQUE", a)
    d.text((MX, 310), "Interdit à la location", font=SERIF(70), fill=A(TXT, a))
    items = [("2025", "G", 9.5, "déjà en vigueur"), ("2028", "F", 12.1, "prévu"), ("2034", "E", 14.4, "prévu")]
    x0 = MX + 40
    d.line([x0 + 60, 480, x0 + 60, 1250], fill=A(CHIPB, a), width=4)
    for i, (yr, lt, t0, sub) in enumerate(items):
        q = a * eo((t - t0) / .35)
        if q <= 0: continue
        y = 520 + i * 260
        s = max(.4, back((t - t0) / .45))
        badge(d, x0 + 60, y + 60, 62, lt, q, s)
        d.text((x0 + 170, y + 10), yr, font=SERIF_I(100), fill=A(TXT, q))
        d.text((x0 + 175, y + 125), sub, font=MONO(22), fill=A(DIM, q))
    if t > 15.2:
        q = a * eo((t - 15.2) / .35)
        st = Image.new("RGBA", (640, 130), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
        sd.rectangle([4, 4, 636, 126], outline=A(LIME, q), width=6)
        sd.text((320, 65), "SUPPRIMÉ ?", font=COND(80), fill=A(LIME, q), anchor="mm")
        st = st.rotate(5, expand=True, resample=Image.BICUBIC)
        L.alpha_composite(st, (300, 1210))

def sc4(L, d, t):
    a = win(t, 16.15, 19.35)
    if not a: return
    label(d, "04  ·  QUI EST CONCERNÉ ?", "ONRE / SDES, PARC AU 1ER JANVIER 2025", a)
    p = eio((t - 16.3) / 1.6)
    v = 1.147 * p
    d.text((MX, 330), f"{v:.1f}".replace(".", ",") + " million", font=SERIF_I(120), fill=A(GOLD, a))
    d.text((MX, 490), "de logements loués", font=SERIF(70), fill=A(TXT, a))
    d.text((MX, 580), "classés F ou G", font=SERIF(70), fill=A(TXT, a))
    # 100 maisons, 14 en rouge
    n = int(100 * eio((t - 16.5) / 1.6))
    for i in range(n):
        r, c = divmod(i, 10)
        x = MX + 40 + c * 78; y = 730 + r * 58
        col = RED if i < 14 else (60, 60, 64)
        d.polygon([(x, y + 18), (x + 26, y), (x + 52, y + 18)], fill=A(col, a))
        d.rectangle([x + 6, y + 18, x + 46, y + 48], fill=A(col, a))
    d.text((MX, 1330), "soit 13,8 % des locations privées", font=MONO(24), fill=A(DIM, a))

def sc5(L, d, t):
    a = win(t, 19.45, 24.8)
    if not a: return
    label(d, "05  ·  POUR LES PROPRIÉTAIRES", "", a)
    d.text((MX, 320), "Un gros", font=SERIF(96), fill=A(TXT, a))
    sc = max(.5, back((t - 20.5) / .5))
    d.text((MX, 430), "soulagement", font=SERIF_I(int(124 * sc)), fill=A(LIME, a))
    for i, (txt, t0) in enumerate([("moins de travaux", 21.9), ("dans l'urgence", 21.9), ("moins de ventes", 23.4), ("contraintes", 23.4)]):
        pass
    for i, (l1, l2, t0) in enumerate([("moins de travaux", "dans l'urgence", 21.9), ("moins de ventes", "contraintes", 23.4)]):
        q = a * eo((t - t0) / .35)
        if q <= 0: continue
        y = 680 + i * 290
        bob = -abs(math.sin((t - t0) * 6)) * 18 * max(0, 1 - (t - t0) / 1.2)
        d.rectangle([MX, y + bob, W - MX, y + 230 + bob], fill=A(CHIP, q), outline=A(LIME, q), width=3)
        check(d, MX + 40, y + 70 + bob, 90, LIME, q)
        d.text((MX + 170, y + 50 + bob), l1, font=SERIF(64), fill=A(TXT, q))
        d.text((MX + 170, y + 130 + bob), l2, font=SERIF_I(64), fill=A(GOLD, q))

def sc6(L, d, t):
    a = win(t, 24.9, 30.7)
    if not a: return
    label(d, "06  ·  PAS ENCORE LA LOI", "EN ATTENDANT, LES RÈGLES ACTUELLES S'APPLIQUENT", a)
    d.text((MX, 300), "Ce n'est pas", font=SERIF(90), fill=A(TXT, a))
    d.text((MX, 410), "encore la loi.", font=SERIF_I(100), fill=A(RED, a))
    steps = [("17 NOV.", "vote de l'amendement", 25.2, True), ("24 NOV.", "vote final des députés", 26.4, False),
             ("DÉC.", "accord avec le Sénat", 28.4, False), ("ENSUITE", "promulgation", 28.9, False)]
    for i, (dt, txt, t0, done) in enumerate(steps):
        q = a * eo((t - t0) / .35)
        if q <= 0: continue
        y = 600 + i * 150
        cx = MX + 40
        if done:
            d.ellipse([cx - 30, y - 30 + 40, cx + 30, y + 30 + 40], fill=A(LIME, q)); check(d, cx - 18, y + 24, 36, (15, 15, 15), q)
        else:
            d.ellipse([cx - 30, y + 10, cx + 30, y + 70], outline=A(DIM, q), width=4)
        if i < 3: d.line([cx, y + 74, cx, y + 160], fill=A(CHIPB, q), width=4)
        d.text((MX + 110, y + 4), dt, font=MONO(24), fill=A(GOLD if not done else LIME, q))
        d.text((MX + 110, y + 40), txt, font=SERIF(50), fill=A(TXT, q))
    if t > 29.4:
        q = a * eo((t - 29.4) / .3)
        sc = max(.5, back((t - 29.4) / .45))
        d.rounded_rectangle([MX, 1220, W - MX, 1330], 16, fill=A((60, 20, 16), q), outline=A(RED, q), width=3)
        d.text((W / 2, 1275), "le gouvernement est contre", font=COND(int(50 * sc)), fill=A(TXT, q), anchor="mm")

def sc7(L, d, t):
    a = win(t, 30.8, 34.1, fout=0.5)
    if not a: return
    label(d, "07  ·  NEWSLETTER GRATUITE", "ON SUIT LE TEXTE JUSQU'AU BOUT", a)
    d.text((MX, 400), "Tu veux savoir", font=SERIF(84), fill=A(TXT, a))
    d.text((MX, 505), "ce qui sera voté ?", font=SERIF_I(90), fill=A(GOLD, a))
    x0, y0, x1, y1 = MX, 760, W - MX, 890
    d.rectangle([x0, y0, x1, y1], fill=A(CHIP, a), outline=A(CHIPB, a), width=2)
    d.text((x0 + 24, y0 + 16), "COMMENTAIRE", font=MONO(17), fill=A(DIM, a))
    word = "DPE"
    typed = word[:int(cl((t - 30.9) / 0.6) * len(word))]
    cur = "|" if int(t * 2.5) % 2 == 0 else " "
    d.text((x0 + 24, y0 + 46), typed + cur, font=SERIF(58), fill=A(GOLD, a))
    d.text((x1 - 24, (y0 + y1) / 2 + 8), "PUBLIER", font=MONO(22), fill=A(TXT if typed == word else DIM, a), anchor="rm")
    bob = math.sin(t * 5) * 10
    d.polygon([(W / 2 - 22, 970 + bob), (W / 2 + 22, 970 + bob), (W / 2, 1002 + bob)], fill=A(DIM, a))

def end_card(L, d, t):
    if t < 34.15: return
    a = eo((t - 34.15) / 0.5)
    d.text((W / 2, 880), "Commente DPE", font=SERIF_I(80), fill=A(GOLD, a), anchor="mm")
    d.text((W / 2, 970), "pour recevoir la newsletter", font=SERIF(44), fill=A(TXT, a), anchor="mm")
    for i, line in enumerate(["Contenu éducatif, pas un conseil personnalisé.",
                              "Texte non définitif : les règles actuelles s'appliquent.",
                              "Sources : AFP, Batiweb (18/11/2026), ONRE/SDES (nov. 2025)."]):
        d.text((W / 2, 1580 + i * 34), line, font=MONO(18), fill=A(DIM2, a), anchor="mm")

run([sc1, sc2, sc3, sc4, sc5, sc6, sc7, end_card], [0, 2.7, 9.3, 16.15, 19.45, 24.9, 30.8, 34.15], "voix_fl.mp3")
