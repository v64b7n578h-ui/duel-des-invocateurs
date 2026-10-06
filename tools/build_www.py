"""Prépare le dossier www/ embarqué dans l'appli Android/iPhone (Capacitor)."""
import pathlib, shutil
R = pathlib.Path(__file__).resolve().parent.parent
W = R / 'www'
if W.exists(): shutil.rmtree(W)
W.mkdir()
for f in ['index.html', 'manifest.webmanifest', 'icon-180.png', 'icon-192.png', 'icon-512.png', 'privacy.html']:
    if (R / f).exists(): shutil.copy(R / f, W / f)
shutil.copytree(R / 'art', W / 'art')
shutil.copytree(R / 'vendor', W / 'vendor')
print('www/ prêt :', sum(1 for _ in W.rglob('*') if _.is_file()), 'fichiers')
