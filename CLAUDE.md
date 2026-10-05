# Duel des Invocateurs — mémo pour reprendre le travail

Projet d'un débutant (francophone) : jeu mobile de duels magiques en temps réel, façon Clash Royale,
avec des personnages illustrés générés sur ChatGPT. Réponds en français, simplement, étape par étape.

## Liens
- Jeu public (GitHub Pages, branche `main`, racine) : https://v64b7n578h-ui.github.io/duel-des-invocateurs/
- Version Claude (artifact) : https://claude.ai/artifact/KDRdjksT4ozFEcwHABV4HJ

## Fichiers
- `index.html` : le jeu complet (HTML/CSS/JS dans un seul fichier, canvas 2D), version installable (manifest, icônes).
- `sources/jeu-version-claude.html` : même jeu sans `<head>` — c'est ce fichier qu'on publie comme artifact.
  Toute modification du jeu doit être faite dans les DEUX fichiers (ou régénérer `index.html` à partir de celui-ci
  en ajoutant l'en-tête PWA présent en haut de `index.html`).
- `art/` : images du jeu détourées en WebP (personnages, arènes `arena*.webp`, tours, portraits `foe1-8`, avatars `av1-8`, pièce `coin*`, packs `pack1-5`).
- `sources/images-originales/` : images ChatGPT d'origine (JPG haute qualité).
- `sources/prompts-personnages.md` : prompts utilisés.

## Ce qui existe dans le jeu
Combat temps réel (3 tours/camp, élixir, deck de 8), 26 personnages avec attaque + pouvoir ultime,
4 fusions, 6 arènes, niveau joueur, trophées, Éveil (3 évolutions), monnaie premium « Invok »,
boutique (personnages, coffres, packs, effets d'invocation, bonus), coffre du jour, 3 quêtes/jour,
Grimoire de saison (30 paliers gratuit + premium), profil et avatars, plein écran / ajout à l'écran d'accueil.
Achats réels non branchés (gratuits en démo). Sauvegarde : localStorage du navigateur (clé `invoc-cr`).

## Méthode pour les nouvelles images
- Demander à ChatGPT un fond NOIR UNI (#000000) ; ses « fonds transparents » sont des damiers dessinés.
- Nouvelle arène : joindre `art/arena.webp` d'origine (941×1672) et demander EXACTEMENT la même disposition
  (rivière au centre, 2 ponts, 6 socles) — la géométrie du jeu est calée dessus (`W=941/47`, `BR`, `RV0/RV1`).

## Prochaines étapes prévues
1. Faire tester à des amis, recueillir leurs retours, équilibrer.
2. Modèles 3D animés (Meshy / Tripo) à partir des images originales.
3. Portage Unity + AdMob + achats intégrés, publication Play Store / App Store.
