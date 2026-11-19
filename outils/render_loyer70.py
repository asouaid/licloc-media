"""NOIR A (Victoria, noir/doré) : les banques ne retiennent que 70 % des loyers."""
import sys; sys.path.insert(0, "/home/claude")
from noirbase import *

def sc1(L, d, t):
    a = win(t, 0, 3.3)
    if not a: return
    label(d, "01  ·  TON DOSSIER DE CRÉDIT", "INVESTISSEMENT LOCATIF", a)
    d.text((MX, 320), "Ton loyer de", font=SERIF(90), fill=A(TXT, a))
    sc = 1 + 0.05 * math.sin(min(t, 1.4) * 2.2)
    d.text((MX, 420), "800 €,", font=SERIF_I(int(170 * sc)), fill=A(GOLD, a))
    d.text((MX, 640), "ta banque le", font=SERIF(80), fill=A(TXT, a))
    d.text((MX, 740), "compte combien ?", font=SERIF_I(96), fill=A(TXT, a))
    for i in range(16):
        r, c = divmod(i, 4)
        wob = math.sin(t * 3 + i) * 6
        bill(L, MX + 120 + c * 200, 960 + r * 90 + wob, 170, 70, GOLD, a)

def sc2(L, d, t):
    a = win(t, 3.35, 10.75)
    if not a: return
    label(d, "02  ·  LA DÉCOTE", "LOYERS RETENUS À 70 %  ·  MEILLEURTAUX, NOV. 2026", a)
    p = eio((t - 3.5) / 0.8)
    v = 800 - 240 * p
    d.text((MX, 320), eur(v), font=SERIF_I(170), fill=A(GOLD, a))
    d.text((MX, 540), "comptés sur 800 €", font=SERIF(64), fill=A(DIM, a))
    # 16 billets dont 5 s'envolent (30 %)
    for i in range(16):
        r, c = divmod(i, 4)
        x, y = MX + 120 + c * 200, 700 + r * 90
        if i >= 11:
            k = i - 11
            q = eio((t - 4.7 - k * 0.25) / 0.9)
            x += q * (300 + k * 40); y -= q * (420 + k * 60)
            bill(L, x, y, 170, 70, DIM, a * (1 - q * .85), rot=q * (25 + k * 12))
        else:
            bill(L, x, y, 170, 70, GOLD, a)
    for j, (txt, t0) in enumerate([("mois vides", 8.4), ("impayés", 9.3), ("charges", 10.1)]):
        q = a * eo((t - t0) / .3)
        if q <= 0: continue
        x = MX + j * 300
        d.rectangle([x, 1150, x + 270, 1230], fill=A(CHIP, q), outline=A(RED, q), width=2)
        d.text((x + 135, 1190), txt, font=MONO(26), fill=A(RED, q), anchor="mm")
    d.text((MX, 1290), "70 % retenus, 30 % de marge de sécurité", font=MONO(22), fill=A(DIM2, a))

def sc3(L, d, t):
    a = win(t, 10.85, 16.1)
    if not a: return
    label(d, "03  ·  EXEMPLE ILLUSTRATIF", "", a)
    d.text((MX, 320), "Exemple", font=SERIF_I(120), fill=A(GOLD, a))
    for i, (lab, val, t0) in enumerate([("SALAIRE NET", "3 000 € / mois", 11.7), ("LOYER DU BIEN", "800 € / mois", 12.4), ("CRÉDIT, ASSURANCE COMPRISE", "1 300 € / mois", 13.3)]):
        q = a * eo((t - t0) / .3)
        if q <= 0: continue
        s = max(.6, back((t - t0) / .4))
        y = 560 + i * 220
        d.rectangle([MX, y, W - MX, y + 180], fill=A(CHIP, q), outline=A(CHIPB, q), width=2)
        d.text((MX + 30, y + 26), lab, font=MONO(22), fill=A(DIM, q))
        d.text((MX + 30, y + 66), val, font=SERIF(int(80 * s)), fill=A(TXT, q))

def gauge(d, y, lab, formula, val, t0, col, a, verdict, tv):
    q = a * eo((t0 and 1) and 1)
    d.text((MX, y), lab, font=COND(46), fill=A(TXT, a))
    d.text((MX, y + 64), formula, font=MONO(22), fill=A(DIM, a))
    x0, x1 = MX, W - MX; yb = y + 110
    d.rectangle([x0, yb, x1, yb + 70], fill=A(CHIP, a), outline=A(CHIPB, a), width=2)
    span = 50.0
    def X(p): return x0 + (x1 - x0) * p / span
    p = val * eio((tv[0] - t0) / 1.0)
    if p > 0:
        d.rectangle([x0 + 3, yb + 3, max(x0 + 4, X(p)), yb + 67], fill=A(col, a))
    lx = X(35)
    d.line([lx, yb - 18, lx, yb + 88], fill=A(TXT, a), width=4)
    d.text((lx, yb - 26), "35 %", font=MONO(22), fill=A(TXT, a), anchor="mb")
    if p > 0:
        d.text((x0 + 20, yb + 35), f"{p:.1f} %".replace(".", ","), font=COND(44), fill=A((12, 12, 12), a), anchor="lm")
    if verdict and tv[0] > tv[1]:
        qq = a * eo((tv[0] - tv[1]) / .3)
        s = max(.5, back((tv[0] - tv[1]) / .45))
        d.text((W - MX, yb + 100), verdict, font=SERIF_I(int(64 * s)), fill=A(col, qq), anchor="ra")

def sc4(L, d, t):
    a = win(t, 16.2, 25.6)
    if not a: return
    label(d, "04  ·  TAUX D'ENDETTEMENT", "PLAFOND HCSF : 35 % ASSURANCE COMPRISE", a)
    gauge(d, 330, "LOYER ENTIER", "1 300 / (3 000 + 800)", 34.2, 17.6, GREEN, a, "ça passe", (t, 19.7))
    if t > 20.5:
        a2 = a * eo((t - 20.5) / .3)
        gauge(d, 760, "LOYER À 70 %", "1 300 / (3 000 + 560)", 36.5, 21.0, RED, a2, "au-dessus", (t, 23.6))

def sc5(L, d, t):
    a = win(t, 25.65, 27.9)
    if not a: return
    label(d, "05  ·  LA LEÇON", "", a)
    d.text((MX, 520), "Fais toujours", font=SERIF(96), fill=A(TXT, a))
    d.text((MX, 640), "ton calcul", font=SERIF(96), fill=A(TXT, a))
    q = eo((t - 26.6) / .3)
    d.text((MX, 790), "avec la décote.", font=SERIF_I(110), fill=A(GOLD, a * q))

def sc6(L, d, t):
    a = win(t, 28.0, 31.42, fout=0.5)
    if not a: return
    label(d, "06  ·  NEWSLETTER GRATUITE", "UN CALCUL PAR SEMAINE", a)
    d.text((MX, 400), "Tu veux d'autres", font=SERIF(84), fill=A(TXT, a))
    d.text((MX, 505), "règles des banques ?", font=SERIF_I(86), fill=A(GOLD, a))
    x0, y0, x1, y1 = MX, 760, W - MX, 890
    d.rectangle([x0, y0, x1, y1], fill=A(CHIP, a), outline=A(CHIPB, a), width=2)
    d.text((x0 + 24, y0 + 16), "COMMENTAIRE", font=MONO(17), fill=A(DIM, a))
    word = "LOYER"
    typed = word[:int(cl((t - 28.1) / 0.7) * len(word))]
    cur = "|" if int(t * 2.5) % 2 == 0 else " "
    d.text((x0 + 24, y0 + 46), typed + cur, font=SERIF(58), fill=A(GOLD, a))
    d.text((x1 - 24, (y0 + y1) / 2 + 8), "PUBLIER", font=MONO(22), fill=A(TXT if typed == word else DIM, a), anchor="rm")
    bob = math.sin(t * 5) * 10
    d.polygon([(W / 2 - 22, 970 + bob), (W / 2 + 22, 970 + bob), (W / 2, 1002 + bob)], fill=A(DIM, a))

def end_card(L, d, t):
    if t < 31.47: return
    a = eo((t - 31.47) / 0.5)
    d.text((W / 2, 880), "Commente LOYER", font=SERIF_I(80), fill=A(GOLD, a), anchor="mm")
    d.text((W / 2, 970), "pour recevoir la newsletter", font=SERIF(44), fill=A(TXT, a), anchor="mm")
    for i, line in enumerate(["Contenu éducatif, pas un conseil personnalisé.",
                              "Exemple illustratif ; pratiques variables selon les banques.",
                              "Sources : Meilleurtaux (nov. 2026), Manda (2026), HCSF."]):
        d.text((W / 2, 1580 + i * 34), line, font=MONO(18), fill=A(DIM2, a), anchor="mm")

run([sc1, sc2, sc3, sc4, sc5, sc6, end_card], [0, 3.35, 10.85, 16.2, 25.65, 28.0, 31.47], "voix_vic.mp3")
