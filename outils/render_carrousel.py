import os; os.environ["VID"]="v1"
import render_ven as R
from PIL import Image, ImageDraw
W,H=1080,1350; MX=90
SERIF,SI,COND,MONO=R.SERIF,R.SERIF_I,R.COND,R.MONO
TXT,DIM,GOLD,RED,GREEN,CHIP,CHIPB=R.TXT,R.DIM,R.GOLD,R.RED,R.GREEN,R.CHIP,R.CHIPB
bg=R.BG.convert("RGB").crop((0,285,1080,1635))
def m(C,r,n=25):
    i=r/1200;N=n*12;return C*i/(1-(1+i)**-N)
def slide(n,tag):
    im=bg.copy();d=ImageDraw.Draw(im)
    d.text((MX,70),f"{n:02d}  ·  {tag}",font=MONO(23),fill=DIM)
    d.text((W-MX,70),f"{n}/7",font=MONO(23),fill=DIM,anchor="ra")
    if n<7: d.text((MX,1262),"Source : baromètre Pretto, novembre 2026. Taux moyens, hors assurance.",font=MONO(18),fill=DIM)
    return im,d
def row(d,y,cols,xs,fonts,fills):
    for c,x,f,fl in zip(cols,xs,fonts,fills):
        d.text((x,y),c,font=f,fill=fl,anchor="ra" if x>MX else "la")
def line(d,y): d.line([MX,y,W-MX,y],fill=CHIPB,width=2)
p=lambda v:f"{v:.2f}".replace(".",",")+" %"
e=lambda v:f"{round(v):,}".replace(","," ")+" €"
S=[]
i,d=slide(1,"LA FICHE À GARDER")
d.text((MX,300),"Tu paies quel taux",font=SERIF(104),fill=TXT)
d.text((MX,430),"en novembre ?",font=SI(116),fill=GOLD)
d.text((MX,640),"3,85 %",font=SI(230),fill=RED)
d.text((MX,920),"le taux moyen sur 25 ans.",font=SERIF(56),fill=TXT)
d.text((MX,1000),"Durée, revenus, mensualité : tout est ici.",font=MONO(27),fill=DIM)
S.append(i)
i,d=slide(2,"PAR DURÉE")
d.text((MX,170),"Plus d'un demi-point",font=SERIF(76),fill=TXT);d.text((MX,265),"depuis l'hiver.",font=SI(80),fill=GOLD)
xs=[MX,560,770,990]
y=470;row(d,y,["DURÉE","T1 2026","NOV.","ÉCART"],xs,[MONO(24)]*4,[DIM]*4);line(d,y+50)
for k,(n,a,b) in enumerate([(15,3.08,3.56),(20,3.17,3.76),(25,3.24,3.85)]):
    y=560+k*170
    row(d,y,[f"{n} ans",p(a),p(b),f"+{(b-a):.2f}".replace(".",",")],xs,[SERIF(64),SERIF(46),SERIF(46),SERIF(46)],[TXT,GREEN,RED,GOLD]);line(d,y+120)
d.text((MX,1120),"Écart en points de pourcentage.",font=MONO(22),fill=DIM)
S.append(i)
i,d=slide(3,"PAR REVENUS")
d.text((MX,170),"Tes revenus changent",font=SERIF(76),fill=TXT);d.text((MX,265),"ton taux.",font=SI(80),fill=GOLD)
xs=[MX,720,990]
y=470;row(d,y,["REVENUS / AN","20 ANS","25 ANS"],xs,[MONO(24)]*3,[DIM]*3);line(d,y+50)
for k,(n,a,b) in enumerate([("Moins de 40 k€",3.91,4.07),("40 à 80 k€",3.85,3.97),("80 à 120 k€",3.80,3.82),("Plus de 120 k€",3.47,3.53)]):
    y=550+k*140
    row(d,y,[n,p(a),p(b)],xs,[SERIF(52),SERIF(52),SERIF(52)],[TXT,TXT,RED if b>=4 else GOLD]);line(d,y+100)
d.text((MX,1130),"Sous 40 000 € par an, le 25 ans passe la barre des 4 %.",font=MONO(24),fill=DIM)
S.append(i)
i,d=slide(4,"LA MENSUALITÉ")
d.text((MX,170),"Sur 200 000 €",font=SERIF(76),fill=TXT);d.text((MX,265),"et 25 ans.",font=SI(80),fill=GOLD)
xs=[MX,640,990]
y=470;row(d,y,["TAUX","PAR MOIS","INTÉRÊTS"],xs,[MONO(24)]*3,[DIM]*3);line(d,y+50)
for k,r in enumerate([3.24,3.53,3.85,4.07]):
    y=550+k*140;c=m(200000,r)
    row(d,y,[p(r),e(c),e(c*300-200000)],xs,[SERIF(56),SERIF(56),SERIF(50)],[TXT,GOLD,RED]);line(d,y+100)
d.text((MX,1130),"Exemple illustratif, calcul hors assurance.",font=MONO(24),fill=DIM)
S.append(i)
i,d=slide(5,"POURQUOI ÇA MONTE")
d.text((MX,170),"Trois raisons",font=SERIF(76),fill=TXT);d.text((MX,265),"en octobre.",font=SI(80),fill=GOLD)
for k,(a,b,c) in enumerate([("+ de 5 %","OAT 10 ans le 21 octobre,","du jamais-vu depuis 2002."),("2,50 %","taux de dépôt de la BCE,","après deux hausses en 2026."),("+ 0,20 pt","et plus sur les grilles","de plusieurs banques.")]):
    y=470+k*240
    d.rectangle([MX,y,W-MX,y+205],fill=CHIP,outline=CHIPB,width=2)
    d.text((MX+30,y+102),a,font=SI(68),fill=RED,anchor="lm")
    d.text((470,y+66),b,font=SERIF(38),fill=TXT);d.text((470,y+114),c,font=SERIF(38),fill=DIM)
S.append(i)
i,d=slide(6,"LES REPÈRES")
d.text((MX,170),"Trois chiffres",font=SERIF(76),fill=TXT);d.text((MX,265),"à connaître.",font=SI(80),fill=GOLD)
for k,(a,b,c) in enumerate([("5,40 %","taux d'usure, prêts de 20 ans","et plus, depuis le 1er octobre."),("+ 0,10 pt","environ pour les","primo-accédants."),("3,47 %","meilleur taux, 80-120 k€,","couple, 20 ans (exemple Pretto).")]):
    y=470+k*240
    d.rectangle([MX,y,W-MX,y+205],fill=CHIP,outline=CHIPB,width=2)
    d.text((MX+30,y+102),a,font=SI(68),fill=GOLD,anchor="lm")
    d.text((470,y+66),b,font=SERIF(36),fill=TXT);d.text((470,y+114),c,font=SERIF(36),fill=DIM)
S.append(i)
i,d=slide(7,"À GARDER")
d.text((W/2,340),"Enregistre cette fiche",font=SERIF(84),fill=TXT,anchor="mm")
d.text((W/2,450),"avant ton rendez-vous banque.",font=SI(68),fill=GOLD,anchor="mm")
d.text((W/2,590),"Envoie-la à quelqu'un qui veut acheter.",font=SERIF(46),fill=TXT,anchor="mm")
d.rectangle([MX,720,W-MX,870],fill=CHIP,outline=GOLD,width=2)
d.text((W/2,795),"Commente CRÉDIT",font=SI(72),fill=GOLD,anchor="mm")
d.text((W/2,930),"pour recevoir la newsletter gratuite",font=SERIF(42),fill=TXT,anchor="mm")
d.text((W/2,1180),"Contenu éducatif, pas un conseil personnalisé.",font=MONO(20),fill=DIM,anchor="mm")
d.text((W/2,1214),"Source : baromètre Pretto, novembre 2026.",font=MONO(20),fill=DIM,anchor="mm")
S.append(i)
os.makedirs("caro",exist_ok=True)
sh=Image.new("RGB",(360*4,450*2))
for k,im in enumerate(S):
    im.save(f"caro/{k+1:02d}.png");sh.paste(im.resize((360,450)),((k%4)*360,(k//4)*450))
sh.save("caro_sheet.png")
