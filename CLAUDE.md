# Duel des Invocateurs — mémo pour reprendre le travail

Projet d'un débutant (francophone) : jeu mobile de duels magiques en temps réel, façon Clash Royale,
avec des personnages illustrés générés sur ChatGPT. Réponds en français, simplement, étape par étape.

## Liens
- Jeu public (GitHub Pages, branche `main`, racine) : https://v64b7n578h-ui.github.io/duel-des-invocateurs/
- Version Claude (artifact) : https://claude.ai/artifact/KDRdjksT4ozFEcwHABV4HJ

## Fichiers
- `index.html` : le jeu complet (HTML/CSS/JS dans un seul fichier, canvas 2D), version installable (manifest, icônes).
- `sources/jeu-version-claude.html` : LA SOURCE du jeu (sans `<head>`), c'est elle qu'on modifie et qu'on publie comme artifact.
  Après chaque modification : `python3 tools/build.py` régénère `index.html` (ajoute l'en-tête PWA de `tools/entete-pwa.html`).
- `art/` : images du jeu détourées en WebP (personnages, arènes `arena*.webp`, tours, portraits `foe1-8`, avatars `av1-8`, pièce `coin*`, packs `pack1-5`).
- `sources/images-originales/` : images ChatGPT d'origine (JPG haute qualité).
- `sources/prompts-personnages.md` : prompts utilisés.

## Applis mobiles (Capacitor 8)
- `capacitor.config.json` (appId `io.github.v64b7n578hui.invocateurs`), projets natifs `android/` et `ios/`.
- `npm run build` : régénère `index.html` puis `www/` (copie embarquée dans l'appli). `npx cap sync` copie `www/` dans les projets natifs.
- `.github/workflows/applis.yml` : à chaque push, GitHub fabrique l'APK Android de test (artefact) et vérifie la compilation iPhone.
- `.github/workflows/appstore.yml` : envoi manuel sur TestFlight (signature automatique via clé API App Store Connect ;
  secrets GitHub APPLE_TEAM_ID, ASC_KEY_ID, ASC_ISSUER_ID, ASC_KEY_P8). Le numéro de build = numéro du run.
- Dans l'appli (`NATIVE` vrai) : les faux packs en € et la fausse pub sont masqués (achats réels pas encore branchés).
- `privacy.html` : politique de confidentialité (URL publique pour les stores). `store/fiche-store.md` : textes des stores.

## Ce qui existe dans le jeu
Écran de chargement, accueil « citadelle » façon jeu de village (HUD niveau/ressources, gros boutons COMBAT/BOUTIQUE,
château qui produit de l'or hors ligne, bulle à récolter), recherche d'adversaire + écran VS.
Nouveau joueur : 6 cartes de base (`STARTER`) + choix de 2 héros parmi `HEROES`, puis visite guidée (`TUT`) ; guide des règles (`HELP`, bouton Aide).
Tous les autres personnages : table `NEWREQ` (gratuit au niveau de joueur `lv` ou tout de suite pour `gems` Invoks). Les coffres ne donnent que des copies.
Sons/musique synthétisés (Web Audio, `sfx()`, `setMood()`), vibrations, réglages dans le Profil. Coffres à minuteur : 4 emplacements
(`S.slots`, `CTYPES`, un seul déverrouillage à la fois, ouverture immédiate en Invoks). Difficulté adaptative (`G.aiK` : 3 premiers
combats et séries de défaites).
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
