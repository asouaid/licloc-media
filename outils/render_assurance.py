"""NOIR B : assurance emprunteur, banque 32 €/mois vs externe 10 €/mois (devis Selectra), loi Lemoine."""
import sys; sys.path.insert(0, "/home/claude")
from noirbase import *

def check(d, x, y, s, col, a):
    d.line([x, y + s * .5, x + s * .38, y + s * .88, x + s, y + s * .1], fill=A(col, a), width=max(4, int(s / 7)), joint="curve")

def shield(d, cx, cy, s, col, a):
    pts = [(cx, cy - s), (cx + s * .8, cy - s * .65), (cx + s * .7, cy + s * .25), (cx, cy + s), (cx - s * .7, cy + s * .25), (cx - s * .8, cy - s * .65)]
    d.polygon(pts, fill=A(tuple(int(c * .35) for c in col), a), outline=A(col, a), width=5)

def sc1(L, d, t):
    a = win(t, 0, 3.0)
    if not a: return
    label(d, "01  ·  ASSURANCE EMPRUNTEUR", "LE COÛT CACHÉ DE TON CRÉDIT", a)
    d.text((MX, 320), "Ton assurance", font=SERIF(100), fill=A(TXT, a))
    d.text((MX, 435), "de prêt, tu la paies", font=SERIF(80), fill=A(TXT, a))
    sc = 1 + 0.07 * math.sin(t * 8) * max(0, 1 - t / 1.6)
    d.text((MX, 560), "3 fois", font=SERIF_I(int(190 * sc)), fill=A(RED, a))
    d.text((MX, 790), "trop cher ?", font=SERIF_I(120), fill=A(GOLD, a))
    bob = abs(math.sin(t * 4)) * 24
    shield(d, 810, 1130 - bob, 130, GOLD, a)
    d.text((810, 1120 - bob), "€", font=SERIF(120), fill=A(GOLD, a), anchor="mm")

def sc2(L, d, t):
    a = win(t, 3.05, 8.3)
    if not a: return
    label(d, "02  ·  EXEMPLE DE DEVIS", "SELECTRA, ÉTUDE DE PRIX 2024", a)
    d.text((MX, 320), "Exemple", font=SERIF_I(110), fill=A(GOLD, a))
    d.text((MX, 450), "de devis", font=SERIF(90), fill=A(TXT, a))
    for i, (lab, val, t0) in enumerate([("EMPRUNTEUR", "25 ans", 4.4), ("EMPRUNTÉ", "218 000 €", 6.15), ("DURÉE", "25 ans", 7.4)]):
        q = a * eo((t - t0) / .3)
        if q <= 0: continue
        s = max(.6, back((t - t0) / .4))
        y = 640 + i * 210
        d.rectangle([MX, y, W - MX, y + 170], fill=A(CHIP, q), outline=A(CHIPB, q), width=2)
        d.text((MX + 30, y + 24), lab, font=MONO(22), fill=A(DIM, q))
        d.text((MX + 30, y + 62), val, font=SERIF(int(80 * s)), fill=A(TXT, q))

def coins(d, x, base, n, col, a):
    for i in range(n):
        y = base - i * 14
        d.ellipse([x, y - 18, x + 200, y + 18], fill=A(tuple(int(c * .5) for c in col), a), outline=A(col, a), width=3)

def sc3(L, d, t):
    a = win(t, 8.4, 12.95)
    if not a: return
    label(d, "03  ·  PAR MOIS", "MÊME PRÊT, MÊME EMPRUNTEUR", a)
    base = 1280
    for k, (lab, v, t0, col) in enumerate([("BANQUE", 32, 9.3, RED), ("EXTERNE", 10, 12.0, GREEN)]):
        x = MX + 60 + k * 450
        p = eio((t - t0) / .55)
        n = int(v * p)
        coins(d, x, base, n, col, a)
        d.text((x + 100, base + 60), lab, font=COND(48), fill=A(TXT, a), anchor="mm")
        if p > 0:
            d.text((x + 100, base - n * 14 - 80), f"{n} €", font=SERIF_I(90), fill=A(col if p >= 1 else TXT, a), anchor="mm")
    d.text((MX, 320), "Cotisation", font=SERIF(84), fill=A(TXT, a))
    d.text((MX, 420), "par mois", font=SERIF_I(84), fill=A(GOLD, a))

def sc4(L, d, t):
    a = win(t, 13.0, 17.55)
    if not a: return
    label(d, "04  ·  SUR TOUT LE PRÊT", "22,05 € × 300 MOIS = 6 615 €", a)
    d.text((MX, 330), "22 €", font=SERIF_I(130), fill=A(GOLD, a))
    d.text((MX + 330, 380), "d'écart / mois", font=SERIF(60), fill=A(TXT, a))
    if t > 14.7:
        q = a * eo((t - 14.7) / .3)
        d.text((MX, 520), "× 300 mois", font=SERIF(90), fill=A(TXT, q))
        # 300 cases qui se remplissent
        n = int(300 * eio((t - 14.8) / 1.3))
        for i in range(n):
            r, c = divmod(i, 25)
            x = MX + c * 35; y = 680 + r * 35
            d.rectangle([x, y, x + 28, y + 28], fill=A((70, 60, 30), q), outline=A(GOLD, q * .8), width=1)
    if t > 16.0:
        q = a * eo((t - 16.0) / .3)
        s = max(.5, back((t - 16.0) / .5))
        d.rounded_rectangle([MX, 1150, W - MX, 1340], 20, fill=A((20, 40, 18), q), outline=A(LIME, q), width=4)
        d.text((W / 2, 1245), "6 600 €", font=SERIF_I(int(130 * s)), fill=A(LIME, q), anchor="mm")

def sc5(L, d, t):
    a = win(t, 17.65, 23.5)
    if not a: return
    label(d, "05  ·  LOI LEMOINE (2022)", "RÉSILIATION À TOUT MOMENT", a)
    shield(d, W - MX - 120, 420, 100, LIME, a)
    check(d, W - MX - 165, 380, 90, LIME, a)
    d.text((MX, 320), "Tu peux", font=SERIF(90), fill=A(TXT, a))
    d.text((MX, 430), "changer", font=SERIF_I(120), fill=A(LIME, a))
    items = [("à tout moment", 20.4), ("sans frais", 21.3), ("si garanties équivalentes", 22.0)]
    for i, (txt, t0) in enumerate(items):
        q = a * eo((t - t0) / .3)
        if q <= 0: continue
        y = 680 + i * 190
        d.rectangle([MX, y, W - MX, y + 150], fill=A(CHIP, q), outline=A(CHIPB, q), width=2)
        check(d, MX + 34, y + 38, 72, LIME, q)
        d.text((MX + 140, y + 75), txt, font=SERIF(58), fill=A(TXT, q), anchor="lm")

def sc6(L, d, t):
    a = win(t, 23.55, 25.85)
    if not a: return
    label(d, "06  ·  LA LEÇON", "", a)
    d.text((MX, 520), "Compare", font=SERIF_I(130), fill=A(GOLD, a))
    d.text((MX, 680), "avant de signer…", font=SERIF(90), fill=A(TXT, a))
    q = eo((t - 24.95) / .3)
    d.text((MX, 840), "et même après.", font=SERIF_I(100), fill=A(LIME, a * q))

def sc7(L, d, t):
    a = win(t, 25.9, 29.33, fout=0.5)
    if not a: return
    label(d, "07  ·  NEWSLETTER GRATUITE", "UN CALCUL PAR SEMAINE", a)
    d.text((MX, 400), "Tu veux d'autres", font=SERIF(84), fill=A(TXT, a))
    d.text((MX, 505), "économies cachées ?", font=SERIF_I(88), fill=A(GOLD, a))
    x0, y0, x1, y1 = MX, 760, W - MX, 890
    d.rectangle([x0, y0, x1, y1], fill=A(CHIP, a), outline=A(CHIPB, a), width=2)
    d.text((x0 + 24, y0 + 16), "COMMENTAIRE", font=MONO(17), fill=A(DIM, a))
    word = "ASSURANCE"
    typed = word[:int(cl((t - 26.0) / 0.8) * len(word))]
    cur = "|" if int(t * 2.5) % 2 == 0 else " "
    d.text((x0 + 24, y0 + 46), typed + cur, font=SERIF(58), fill=A(GOLD, a))
    d.text((x1 - 24, (y0 + y1) / 2 + 8), "PUBLIER", font=MONO(22), fill=A(TXT if typed == word else DIM, a), anchor="rm")
    bob = math.sin(t * 5) * 10
    d.polygon([(W / 2 - 22, 970 + bob), (W / 2 + 22, 970 + bob), (W / 2, 1002 + bob)], fill=A(DIM, a))

def end_card(L, d, t):
    if t < 29.38: return
    a = eo((t - 29.38) / 0.5)
    d.text((W / 2, 880), "Commente ASSURANCE", font=SERIF_I(78), fill=A(GOLD, a), anchor="mm")
    d.text((W / 2, 970), "pour recevoir la newsletter", font=SERIF(44), fill=A(TXT, a), anchor="mm")
    for i, line in enumerate(["Contenu éducatif, pas un conseil personnalisé.",
                              "Exemple de devis : tarifs variables selon profil et garanties.",
                              "Source : Selectra, étude de prix 2024 ; loi Lemoine (2022)."]):
        d.text((W / 2, 1580 + i * 34), line, font=MONO(18), fill=A(DIM2, a), anchor="mm")

run([sc1, sc2, sc3, sc4, sc5, sc6, sc7, end_card], [0, 3.05, 8.4, 13.0, 17.65, 23.55, 25.9, 29.38], "voix_fl.mp3")
