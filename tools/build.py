"""Fabrique index.html (version GitHub, installable) à partir de sources/jeu-version-claude.html.
Usage : python3 tools/build.py"""
import pathlib
R = pathlib.Path(__file__).resolve().parent.parent
head = (R / 'tools/entete-pwa.html').read_text()
src = (R / 'sources/jeu-version-claude.html').read_text()
html = head + src.replace('</style>', '</style>\n</head><body>', 1) + '\n</body></html>\n'
(R / 'index.html').write_text(html)
print('index.html régénéré :', len(html), 'caractères')
