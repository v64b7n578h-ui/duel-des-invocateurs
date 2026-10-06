"""Générateur de cartes à collectionner.

Prend une illustration de carte faite sur ChatGPT (cartes/sources/<id>.png, zones vides),
ajoute le coût, le nom, la rareté, les stats et les textes (cartes/cartes.json),
puis produit :
  - cartes/apercu/<id>.png   : la carte finie, pour l'écran et les réseaux
  - cartes/imprimer/<id>.png : fichier imprimeur 63 × 88 mm + 3 mm de fond perdu, 300 dpi

Usage : python3 tools/cartes.py            (toutes les cartes)
        python3 tools/cartes.py dragon     (une seule)
"""
import json, math, sys, pathlib
from PIL import Image, ImageDraw, ImageFilter, ImageFont

R = pathlib.Path(__file__).resolve().parent.parent
F = R / 'tools' / 'fonts'
DPI = 300
MM = DPI / 25.4
CARD_MM, BLEED_MM = (63, 88), 3

def font(name, size):
    return ImageFont.truetype(str(F / name), size)

TITLE = 'grenze-gotisch-latin-800-normal.woff'
B5, B6, B7, B8 = (f'barlow-semi-condensed-latin-{w}-normal.woff' for w in (500, 600, 700, 800))
RARE = {'Commune': (1, '#c9c6d6'), 'Rare': (1, '#6fb7ff'), 'Épique': (1, '#c77dff'),
        'Légendaire': (2, '#ffd56b'), 'Arcane Secrète': (3, '#ffe9a8')}


def star(d, cx, cy, r, fill):
    """Étoile à 4 branches (✦) dessinée à la main : les polices n'ont pas toujours ce symbole."""
    pts = []
    for i in range(8):
        a = -math.pi / 2 + i * math.pi / 4
        rr = r if i % 2 == 0 else r * 0.32
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    d.polygon(pts, fill=fill)


def text_glow(base, xy, txt, fnt, fill, glow, radius=6, anchor='la', stroke=0, stroke_fill=None):
    """Texte avec halo flou derrière (lisible sur un fond holographique chargé)."""
    lay = Image.new('RGBA', base.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).text(xy, txt, font=fnt, fill=glow, anchor=anchor, stroke_width=stroke + 3, stroke_fill=glow)
    base.alpha_composite(lay.filter(ImageFilter.GaussianBlur(radius)))
    ImageDraw.Draw(base).text(xy, txt, font=fnt, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=stroke_fill)


def fit(txt, name, size, maxw, minsize=10):
    while size > minsize and font(name, size).getlength(txt) > maxw:
        size -= 1
    return font(name, size)


def wrap(txt, fnt, maxw):
    lines, cur = [], ''
    for w in txt.split():
        t = (cur + ' ' + w).strip()
        if fnt.getlength(t) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    return lines + ([cur] if cur else [])


def holo_fx(im, z, seed=1):
    """Édition Brillante : cadre doré, reflet holographique arc-en-ciel, rayons et éclats."""
    import numpy as np, random
    rnd = random.Random(seed)
    W, H = im.size
    a = np.asarray(im.convert('RGB')).astype(float)
    mx, mn = a.max(2), a.min(2)
    sat = (mx - mn) / np.maximum(mx, 1)
    # zone de l'illustration (entre le bandeau du nom et l'encadré du bas)
    tx0, ty0, tx1, ty1 = z['texte']
    nx0, ny0, nx1, ny1 = z['nom']
    art = np.zeros((H, W), bool); art[ny1 + 12:ty0 - 10, tx0 + 6:tx1 - 6] = True
    inside_text = np.zeros((H, W), bool); inside_text[ty0 + 10:ty1 - 10, tx0 + 10:tx1 - 10] = True
    card = np.zeros((H, W), bool); cx0, cy0, cx1, cy1 = z['carte']; card[cy0:cy1, cx0:cx1] = True
    # 1) cadre : le métal argenté/bleuté devient or
    frame = card & ~art & ~inside_text & (mx > 60)
    lum = a.mean(2) / 255
    gold = np.stack([255 * (.35 + .75 * lum), 205 * (.25 + .8 * lum), 95 * (.15 + .9 * lum)], 2).clip(0, 255)
    mxc, myc, mr = z['medaillon']
    med = ((X0 := np.arange(W)[None, :]) - mxc) ** 2 + (np.arange(H)[:, None] - myc) ** 2 <= (mr * 1.08) ** 2
    k = np.maximum(frame * np.clip(1.2 - sat * 1.4, 0, 1), med * .85)[..., None] * .92
    a = a * (1 - k) + gold * k
    # 2) reflet holographique en bandes diagonales (sur toute la carte, plus fort sur le cadre)
    Y, X = np.mgrid[0:H, 0:W]
    t = (X * .9 + Y * .55) / 95.0
    rain = np.stack([np.sin(t) * .5 + .5, np.sin(t + 2.1) * .5 + .5, np.sin(t + 4.2) * .5 + .5], 2) * 255
    band = (np.sin((X + Y * .6) / 260.0) * .5 + .5) ** 3
    amt = ((.35 + band * .65) * np.where(frame, .42, .30) * card * ~inside_text)[..., None]
    a = 255 - (255 - a) * (1 - amt * rain / 255)          # mode « superposition écran »
    out = Image.fromarray(a.clip(0, 255).astype('uint8')).convert('RGBA')
    # 3) rayons de lumière derrière le personnage
    rays = Image.new('L', (W, H), 0); dr = ImageDraw.Draw(rays)
    cx, cy = (tx0 + tx1) / 2, ny1 + 60
    for i in range(18):
        ang = math.pi * (.08 + .84 * i / 17) + rnd.uniform(-.03, .03)
        w = rnd.uniform(.025, .05)
        L = 1600
        dr.polygon([(cx, cy), (cx + math.cos(ang - w) * L, cy + math.sin(ang - w) * L), (cx + math.cos(ang + w) * L, cy + math.sin(ang + w) * L)], fill=rnd.randint(55, 110))
    rays = rays.filter(ImageFilter.GaussianBlur(14))
    m = Image.fromarray((np.asarray(rays) * art).astype('uint8'))
    out.alpha_composite(Image.merge('RGBA', (Image.new('L', (W, H), 255), Image.new('L', (W, H), 240), Image.new('L', (W, H), 200), m)))
    # 4) éclats scintillants
    sp = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sp)
    for _ in range(70):
        x, y = rnd.randint(cx0 + 10, cx1 - 10), rnd.randint(cy0 + 10, cy1 - 10)
        if inside_text[y, x]: continue
        r = rnd.choice([6, 8, 10, 14, 20, 28])
        col = rnd.choice([(255, 255, 255), (255, 240, 190), (200, 235, 255), (255, 210, 250)])
        star(ds, x, y, r, col + (rnd.randint(170, 255),))
        ds.ellipse((x - r * .18, y - r * .18, x + r * .18, y + r * .18), fill=(255, 255, 255, 255))
    glow = sp.filter(ImageFilter.GaussianBlur(4))
    out.alpha_composite(glow); out.alpha_composite(sp)
    return out


def render(cid, c, serie, total):
    im = Image.open(R / 'cartes' / 'sources' / f'{c.get("source", cid)}.png').convert('RGBA')
    z = c['zones']
    if c.get('edition') == 'Brillante':
        im = holo_fx(im, z, seed=c['num'])
    d = ImageDraw.Draw(im)
    n_stars, rcol = RARE[c['rarete']]
    if c.get('edition'):
        rcol = '#ffd56b'

    # --- coût dans le médaillon ---
    mx, my, mr = z['medaillon']
    text_glow(im, (mx, my + 4), str(c['cout']), font(TITLE, int(mr * 1.45)), '#ffffff', (120, 40, 200, 255),
              radius=10, anchor='mm', stroke=3, stroke_fill='#3a1466')

    # --- nom dans le bandeau ---
    x0, y0, x1, y1 = z['nom']
    fn = fit(c['nom'], TITLE, int((y1 - y0) * .62), (x1 - x0) - 40)
    text_glow(im, ((x0 + x1) / 2, (y0 + y1) / 2 + 2), c['nom'], fn, '#2a1240', (255, 255, 255, 230), radius=7, anchor='mm')

    # --- encadré du bas : voile sombre puis textes ---
    x0, y0, x1, y1 = z['texte']
    veil = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(veil).rounded_rectangle((x0 + 6, y0 + 6, x1 - 6, y1 - 6), 18, fill=(14, 8, 30, 175))
    im.alpha_composite(veil)
    d = ImageDraw.Draw(im)
    pad, W = 26, (x1 - x0)
    cy = y0 + 32
    for i in range(n_stars):
        star(d, x0 + pad + 12 + i * 26, cy, 12, rcol)
    tx = x0 + pad + n_stars * 26 + 6
    lab = f"{c['rarete'].upper()}  ·  {c['type'].upper()}"
    if c.get('edition'):
        lab = f"ÉDITION {c['edition'].upper()}  ·  " + lab
        rcol = '#ffd56b'
    d.text((tx, cy), lab, font=font(B8, 23), fill=rcol, anchor='lm')
    # stats à droite
    fs, fl = font(B8, 30), font(B7, 19)
    pv, atk = str(c['pv']), str(c['atk'])
    x = x1 - pad
    d.text((x, cy), pv, font=fs, fill='#7ee2a0', anchor='rm'); x -= fs.getlength(pv) + 6
    d.text((x, cy + 2), 'PV', font=fl, fill='#7ee2a0', anchor='rm'); x -= fl.getlength('PV') + 20
    d.text((x, cy), atk, font=fs, fill='#ff9b6b', anchor='rm'); x -= fs.getlength(atk) + 6
    d.text((x, cy + 2), 'ATK', font=fl, fill='#ff9b6b', anchor='rm')
    d.line((x0 + pad, cy + 24, x1 - pad, cy + 24), fill=(232, 185, 74, 160), width=2)

    # attaque puis pouvoir ultime : titre en gras suivi de la description, sur la même ligne
    fh, fb, lh = font(B8, 23), font(B5, 23), 27
    y = cy + 36
    maxx = x1 - pad
    lbl2 = 'Pouvoir ultime' if 'ultime' in c else 'Talent'
    for is_ult, (titre, desc) in ((False, c['attaque']), (True, c.get('ultime') or c['talent'])):
        x = x0 + pad
        if is_ult:
            star(d, x + 8, y + 13, 9, '#ffd56b'); x += 22
        head = (lbl2 + ' — ' if is_ult else '') + titre + ' : '
        d.text((x, y), head, font=fh, fill='#ffd56b' if is_ult else '#ffffff'); x += fh.getlength(head)
        for w in desc.split():
            ww = fb.getlength(w + ' ')
            if x + fb.getlength(w) > maxx:
                y += lh; x = x0 + pad
            d.text((x, y), w, font=fb, fill='#e9e2f7'); x += ww
        y += lh + 4

    # numéro de collection + série, en tout petit
    fsm = font(B6, 16)
    d.text((x0 + pad, y1 - 16), f"{c['num']:03d}/{total:03d}", font=fsm, fill=(220, 210, 240, 190), anchor='lm')
    d.text((x1 - pad, y1 - 16), f'Duel des Invocateurs · {serie}', font=fsm, fill=(220, 210, 240, 190), anchor='rm')
    if y > y1 - 26:
        print(f'  ⚠ {cid} : texte trop long pour l\'encadré, raccourcis la description')

    out_a = R / 'cartes' / 'apercu' / f'{cid}.png'
    im.save(out_a)
    # version pour l'album du jeu (art/cartes/<id>.webp), coupée au contour de la carte
    (R / 'art' / 'cartes').mkdir(exist_ok=True)
    g = im.crop(tuple(z['carte'])).resize((480, 729), Image.LANCZOS)
    g.save(R / 'art' / 'cartes' / f'{cid}.webp', 'WEBP', quality=86, method=6)

    # --- fichier imprimeur ---
    cx0, cy0, cx1, cy1 = z['carte']
    card = im.crop((cx0, cy0, cx1, cy1)).convert('RGB')
    tw, th = round(CARD_MM[0] * MM), round(CARD_MM[1] * MM)
    card = card.resize((tw, th), Image.LANCZOS)
    b = round(BLEED_MM * MM)
    pr = Image.new('RGB', (tw + 2 * b, th + 2 * b))
    pr.paste(card, (b, b))
    # fond perdu : on prolonge les bords de la carte (miroir) sur 3 mm
    pr.paste(card.crop((0, 0, tw, b)).transpose(Image.FLIP_TOP_BOTTOM), (b, 0))
    pr.paste(card.crop((0, th - b, tw, th)).transpose(Image.FLIP_TOP_BOTTOM), (b, th + b))
    col = pr.crop((b, 0, 2 * b, th + 2 * b)).transpose(Image.FLIP_LEFT_RIGHT); pr.paste(col, (0, 0))
    col = pr.crop((tw, 0, tw + b, th + 2 * b)).transpose(Image.FLIP_LEFT_RIGHT); pr.paste(col, (tw + b, 0))
    out_p = R / 'cartes' / 'imprimer' / f'{cid}.png'
    pr.save(out_p, dpi=(DPI, DPI))
    return out_a, out_p, pr.size


if __name__ == '__main__':
    data = json.loads((R / 'cartes' / 'cartes.json').read_text())
    ids = sys.argv[1:] or list(data['cartes'])
    for cid in ids:
        a, p, size = render(cid, data['cartes'][cid], data['serie'], data['total'])
        print(f'{cid}: aperçu {a.name}, impression {size[0]}×{size[1]} px à {DPI} dpi')
