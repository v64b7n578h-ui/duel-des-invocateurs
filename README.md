# Duel des Invocateurs

Prototype de jeu mobile de duels magiques en temps réel (style Clash Royale), avec des personnages inspirés des jeux de cartes à collectionner.

**Version jouable en ligne :** https://claude.ai/artifact/KDRdjksT4ozFEcwHABV4HJ

## Contenu du dossier

| Élément | Rôle |
|---|---|
| `index.html` | Le jeu complet. Ouvre-le dans Chrome ou Firefox, en le laissant à côté du dossier `art/`. |
| `art/` | Les 62 images du jeu, déjà détourées et optimisées (personnages, arènes, tours, portraits, pièce Invok). |
| `originaux-hd/` | Les images d'origine générées avec ChatGPT, en haute qualité (JPG). Ce sont elles qui serviront pour la version Unity. |
| `prompts-personnages.md` | Les prompts des 18 premiers personnages. |

## Ce que contient le jeu

- **Combat en temps réel** : 3 tours par camp, élixir, deck de 8 cartes, cartes qui tournent.
- **26 personnages** chacun avec son attaque, son effet et un **pouvoir ultime** (ralenti, bande façon anime).
- **4 fusions** à découvrir en invoquant une carte sur une troupe compatible.
- **6 arènes** à débloquer : Académie des Arcanes, Forge du Volcan, Citadelle de Givre, Sanctuaire Sylvestre, Temple des Abysses, Cité Céleste.
- **Progression** : niveau de joueur, trophées, ligues, niveaux de cartes, **Éveil** (3 évolutions par personnage).
- **Économie** : or, **Invoks** (monnaie premium), boutique, coffres, packs, effets d'invocation cosmétiques, bonus.
- **Rétention** : coffre du jour avec série, **3 quêtes par jour**, **Grimoire de saison** à 30 paliers (gratuit et premium).
- **Profil** : nom, titre, statistiques, 8 avatars à débloquer.

## Sauvegarde des joueurs

La progression est enregistrée dans le navigateur de chaque joueur (stockage local). Pour un vrai jeu, il faudra un serveur : comptes, achats et classements.

## Prochaines étapes

1. Faire tester le lien à 5 à 10 personnes et noter leurs remarques.
2. Équilibrer les cartes selon leurs retours.
3. Créer des modèles 3D animés (Meshy / Tripo) à partir des images de `originaux-hd/`.
4. Reprendre le jeu dans Unity, brancher AdMob et les achats intégrés, publier sur le Play Store et l'App Store.
