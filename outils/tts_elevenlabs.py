"""Voix ElevenLabs par l'API.
Usage : python3 tts_elevenlabs.py VOICE_ID sortie.mp3 "texte" [modele] [reglages_json]
Clé : variable d'environnement ELEVENLABS_API_KEY, sinon fichier indiqué par ELEVENLABS_KEY_FILE (valeur sk_...). Jamais affichée.
voice_id : Victoria WeAAwKYcS06VmXw086yZ · François Louis UBXZKOKbt62aLQHhc1Jm · Nathan Doré Ayvd8fDj52DfUWXZeAFe · Victor GPAQQPp9dazaB2bl4zg9
"""
import os, re, sys, json, urllib.request, urllib.error
K = os.environ.get("ELEVENLABS_API_KEY", "")
if not K.startswith("sk_"):
    f = os.environ.get("ELEVENLABS_KEY_FILE", "")
    K = re.findall(r"sk_[A-Za-z0-9]{20,}", open(f, errors="ignore").read())[-1] if f else ""
if not K: sys.exit("clé ElevenLabs absente")
vid, out, txt = sys.argv[1], sys.argv[2], sys.argv[3]
model = sys.argv[4] if len(sys.argv) > 4 else "eleven_v4"
st = json.loads(sys.argv[5]) if len(sys.argv) > 5 else {"stability": 0.3, "similarity_boost": 0.85}
body = json.dumps({"text": txt, "model_id": model, "voice_settings": st}).encode()
r = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128", data=body,
                           headers={"xi-api-key": K, "Content-Type": "application/json"})
try:
    d = urllib.request.urlopen(r, timeout=120).read(); open(out, "wb").write(d); print("ok", len(d))
except urllib.error.HTTPError as e:
    print("ERR", e.code, e.read()[:300].decode()); sys.exit(1)
