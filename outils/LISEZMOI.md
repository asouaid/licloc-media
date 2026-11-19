# Gabarits vidéo LICLOC
- NOIR : noirbase.py (commun) + un fichier de scènes par vidéo (render_loyer70.py, render_assurance.py, render_dpe_vote.py, render_levier.py, render_impayes.py). `AUDIO=<durée> THEME=a|b python3 render_x.py sortie.mp4` (ou `stills t1 t2…`). Polices : npm pack @fontsource/oswald @fontsource/source-serif-4 @fontsource/jetbrains-mono → /home/claude/fonts/use/.
- INTÉRIEUR : pipeline-cartoon-v6-interieur.tgz (ep_int.html scene=bureau, specs.py SPK='HM', gen.py, split2.py, rw6.js, comp.py ; three@0.169.0, @fontsource/poppins).
- EXTÉRIEUR : pipeline-cartoon-v5-scenes.tgz (ep6.html, SPK='HFM').
- Voix : tts_elevenlabs.py.
Procédure complète : fichiers du projet Claude LICLOC, `marketing/PROCEDURE-video-du-jour.md`.
