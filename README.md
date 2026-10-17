# TENSION — teaser de 31 s pour la lampe TENSIL

> Statut : **livré** le 2026-10-17. Marque fictive, projet de démonstration pour le portfolio.

![TENSION — chapitre IV, la lumière](export/web/05-lumiere.webp)

## 1. But du projet
Réaliser un teaser publicitaire de 31,5 s, dans les codes d'une marque de luxe, pour **TENSIL**, la lampe de bureau articulée modélisée dans [blender-studio-object](https://github.com/elie-gordo/blender-studio-object). Le film raconte une histoire en quatre chapitres : la lampe au repos, la tension des ressorts, l'équilibre trouvé, puis la lumière.

Il démontre une chaîne de production **hybride** : une préviz Blender sert de référence de mouvement à un modèle vidéo IA (Seedance 2.5), les plans macro sont rendus en 3D, et le montage, le motion design et le mixage sont écrits en code. Voix off et musique sont générées par IA (ElevenLabs, Suno).

Projet réalisé en **duo humain + IA** :
- **Elliott Lanza** : concept « TENSION », storyboard, choix du budget et des versions, ligne de fin, direction du motion design, génération de la voix off et de la musique, validation de chaque étape.
- **Claude (Anthropic, via Claude Code)** : scripts Blender, préparation et lancement des générations Seedance, montage, motion design et mixage dans Remotion, prompts voix et musique, contrôles et documentation.

## 2. Le film
| Temps | Chapitre | Plans | Texte à l'écran (dit en voix off) |
|---|---|---|---|
| 0–1,5 s | prologue | P1 (noir) | « Certains objets attendent. » |
| 1,5–10 s | **I · Repos** | P02 ressort, P03 pivot, P04 lampe pliée | annotations « 01 — Ressort », « 02 — Pivot » ; « Au repos, jamais inerte. » |
| 10–18 s | **II · Tension** | P05 le bras se lève, P06 ressort, P07 la tête bascule | « Toute sa force tient dans la retenue. » ; « 03 — Tension » ; « Elle cède. » |
| 18–23,5 s | **III · Équilibre** | P08 pose de travail, P09 bouton | « Puis trouve sa place. Et n'en bouge plus. » ; « 04 — Interrupteur » |
| 23,5–28 s | **IV · Lumière** | P10 allumage, fin ralentie | « Alors seulement, la lumière. » |
| 27,5–31,5 s | fin | P11 | TENSIL — « Tenue par la tension. » |

Chaque titre est dit en voix off au moment où il apparaît (7 phrases). La musique suit la même courbe : calme au repos, montée sur la tension, sommet à l'allumage, et s'efface sous chaque phrase.

Les caractéristiques des annotations (42 spires, laiton tourné…) sont inventées pour le récit, comme la marque.

## 3. Ce qu'il démontre
- **Préviz au service de l'IA :** chaque plan Seedance reçoit la vidéo de préviz Blender (caméra et timing), une image de début, une image de fin et les rendus produit. Le prompt interdit l'image en miroir et toute modification de la lampe.
- **Pipeline hybride maîtrisé :** 4 plans macro en EEVEE, 5 plans en IA, mêmes caméras et même timeline à 30 i/s (`blender/film.py`).
- **Agent IA relié aux outils :** Claude Code pilote Blender et Higgsfield par MCP : rendus, envoi des références, devis puis génération.
- **Motion design de marque :** format cinéma, barre de chapitres, titres révélés mot par mot, annotations techniques façon film horloger (`edit/src/Story.tsx`).
- **Mixage voix et musique en code :** voix off calée à l'image près sur les titres, musique baissée automatiquement sous la voix (`edit/src/Tension.tsx`).
- **Budget piloté :** coût affiché avant chaque génération, un plan test avant les autres, 72 crédits dépensés.
- **Montage reproductible :** tout le film se reconstruit en commandes.

## 4. Outils
| Outil | Version / mode | Rôle dans le projet |
|---|---|---|
| Claude Code (Claude Opus 5.5) | CLI, Windows 11 | Agent : scripts, pilotage de Blender et de Higgsfield, montage, prompts, contrôles, documentation |
| Blender | 5.2.2 LTS, EEVEE | Scène, caméras, animation de la lampe, préviz, références Seedance, plans macro |
| Script `blender/film.py` | Python (bpy) | Construit la scène, anime la lampe joint par joint, rend chaque plan |
| Extension Higgsfield pour Blender + MCP `higgsfield-bridge` | option « Enable MCP control » | Relie Blender à Claude Code (lecture de scène, rendus, captures) |
| Connecteur MCP Higgsfield | `media_upload`, `generate_video`, `get_cost`, `jobs_wait` | Envoi des références, devis, lancement et suivi des générations |
| Seedance 2.5 (via Higgsfield) | mode `omni_reference`, brouillon 480p | 5 plans vidéo guidés par la préviz |
| Remotion | 4.0.536 (React 18, TypeScript) | Montage, étalonnage, grain, motion design, écran de fin, mixage, rendu H.264 + AAC |
| `@remotion/google-fonts` | Archivo Narrow, Azeret Mono, Inter | Typographie de la marque TENSIL (reprise de la boutique) |
| ffmpeg / ffprobe | fournis par Remotion (`npx remotion ffmpeg`) | Découpe, extraction d'images, vérification des fichiers |
| ElevenLabs | Voice Design + Eleven v3 | Voix off, 7 phrases générées une par une |
| Suno | mode Instrumental | Musique de 60 s, dont 31 s utilisées |
| Python | 3.11, numpy, Pillow | Analyse de la musique et des niveaux, médias web du portfolio |
| Node.js, npm, Git | — | Exécution de Remotion, scripts, versionnage |
| Matériel | RTX 2050 (4 Go de VRAM), 16 Go de RAM | Rendus locaux |

## 5. Étapes de création
1. **Cadrage.** Relecture des projets TENSIL existants (modèle 3D, boutique, campagne), trois concepts proposés, choix de « TENSION » : la lampe tient grâce à ses ressorts. Storyboard de 11 plans sur 30 s.
2. **Connexion des outils.** Connecteur Higgsfield vérifié dans Claude Code. Extension Higgsfield installée dans Blender ; son option « Enable MCP control » était désactivée, elle est activée par script pour que Claude Code pilote Blender.
3. **Préviz Blender** ([`blender/film.py`](blender/film.py)). La lampe du projet Blender est posée dans un studio sombre. Une caméra par plan, animation joint par joint (épaule, coude, tête, interrupteur, ampoule) sur une timeline de 900 images à 30 i/s. Animatic : [`export/animatic/`](export/animatic/).
4. **Répartition des plans.** Les gros plans mécaniques, où l'IA déforme les ressorts, restent en 3D (P02, P03, P06, P09). Les plans d'ensemble, où l'IA apporte le réalisme, vont à Seedance (P04, P05, P07, P08, P10).
5. **Plans macro EEVEE** rendus directement depuis la préviz ([`export/shots/final/`](export/shots/final/)).
6. **Références Seedance** ([`export/shots/ref/`](export/shots/ref/)). Pour chaque plan IA : la vidéo de préviz en 1280×720 avec 0,5 s de marge (Seedance génère 4 s au minimum), une image de début, une image de fin, et 3 ou 4 rendus produit. Un bloc de prompt commun interdit le miroir et toute modification de la lampe ([`storyboard/seedance_shots.md`](storyboard/seedance_shots.md)).
7. **Génération.** Les références sont envoyées sur Higgsfield, le coût est affiché avant chaque lancement. P04 est généré seul en brouillon 480p (15 crédits) pour tester, puis les quatre autres en lot ([`export/shots/draft/`](export/shots/draft/)). Total : 72 crédits.
8. **Contrôle de fidélité.** Début, milieu et fin de chaque plan comparés à la préviz : pas de miroir, pose conforme, pièces présentes.
9. **Montage** ([`edit/`](edit/)). Remotion place chaque plan à l'image près selon `film.py`, retire les marges, étalonne plans IA et plans 3D pour qu'ils se raccordent, ajoute grain et vignettage, et ralentit la fin de P10 à mi-vitesse.
10. **Motion design** ([`edit/src/Story.tsx`](edit/src/Story.tsx)). Bandes cinéma, barre des quatre chapitres, six titres révélés mot par mot, quatre annotations techniques reliées à la pièce, lueur chaude à l'allumage. Chaque texte est placé dans une zone vide du plan, vérifiée sur des images fixes.
11. **Écran de fin** (P11 : TENSIL, « Tenue par la tension. ») et une seconde composition sans écran de fin.
12. **Voix off.** Les textes de la voix sont ceux des titres. Une voix grave et posée est créée avec Voice Design, puis chaque phrase est générée avec Eleven v3 ([`assets/audio/vo/`](assets/audio/vo/)) et placée à l'image près sur l'apparition de son titre.
13. **Musique.** Le prompt est d'abord écrit pour Eleven Music, mais le téléchargement y demande un abonnement : la musique est faite sur Suno, en mode Instrumental, avec le style décrit dans le champ « Style ». Sur les 60 s produites, les 31 premières sont gardées : leur sommet d'énergie (25 s) tombe sur l'allumage (24,95 s) ([`assets/audio/music/`](assets/audio/music/)).
14. **Mixage.** La musique passe de 0,6 à 0,27 sous chaque phrase (attaque 6 images, retour 14 images) et s'éteint sur les 20 dernières images. Le film est allongé à 31,5 s pour laisser finir la dernière phrase. Des bruitages synthétisés ([`script/sound.py`](script/sound.py)) ont été essayés puis retirés : le film garde seulement la voix et la musique.
15. **Exports.** Master, version sans écran de fin, version web légère, image d'aperçu, puis images et vidéo muette du portfolio ([`script/portfolio_media.py`](script/portfolio_media.py)).

### Reproduire
```bash
B="C:/Program Files/Blender Foundation/Blender 5.2/blender.exe"
# préviz, références et macros (voir l'en-tête de blender/film.py)
"$B" -b assets/3d/tensil_lamp.blend --python blender/film.py -- build
"$B" -b blender/tensil_film.blend --python blender/film.py -- shot P02
# montage (Node 18+)
cd edit && npm install
npm run media            # copie plans, voix et musique dans edit/public
npm run typecheck
npm run render           # master 31,5 s
npm run render:no-endcard
npm run render:web
npm run poster
npm run studio           # aperçu interactif
# médias du portfolio (Python avec Pillow)
cd .. && python script/portfolio_media.py
```
Les plans Seedance, la voix et la musique ne se régénèrent pas à l'identique : ils sont versionnés dans `export/shots/draft/` et `assets/audio/`.

## 6. Exports
| Fichier | Format | Contenu |
|---|---|---|
| `export/master/TENSION_master_1080p.mp4` | H.264 + AAC, 1920×1080, 30 i/s, 31,5 s | Film complet avec voix, musique et écran de fin (CRF 16, 14,7 Mo) |
| `export/master/TENSION_no_endcard_1080p.mp4` | idem, 28,5 s | Sans l'écran de fin ni la dernière phrase, fondu au noir après l'allumage |
| `export/master/TENSION_web_1080p.mp4` | idem, CRF 26 | Version web légère avec son (4,4 Mo) |
| `export/master/TENSION_poster.jpg` | JPEG 1920×1080 | Image d'aperçu (écran de fin) |
| `export/web/tension-teaser.mp4` | H.264 sans son, 1080p | Lecture automatique sur le portfolio (2,4 Mo) |
| `export/web/*.webp` | WebP 1600 px | Six images clés, planche des plans, préviz contre Seedance, vignette 1200×675 |

## 7. Structure du dépôt
| Dossier | Contenu |
|---|---|
| `assets/3d/` | Lampe TENSIL reprise du projet Blender |
| `assets/references/` | Rendus produit envoyés à Seedance |
| `assets/audio/` | Voix off (`vo/`) et musique (`music/`) |
| `blender/` | Script et scène de la préviz |
| `storyboard/` | Fiches et prompts Seedance |
| `export/` | Animatic, références, plans, masters, médias web |
| `edit/` | Projet Remotion (montage, motion design, mixage) |
| `script/` | Médias du portfolio, bruitages abandonnés |
| `docs/` | Étude de cas, portfolio, crédits, coûts, suivi |

## 8. Coûts
72 crédits Higgsfield (5 brouillons Seedance 480p), sur un plan Plus. ElevenLabs et Suno en offre gratuite, le reste est gratuit. Voir [docs/COSTS.md](docs/COSTS.md).

## 9. Ressources tierces et licences
Plans Seedance générés avec un plan payant, voix off ElevenLabs et musique Suno en offres gratuites, polices sous licence SIL OFL. Les offres gratuites limitent l'usage à un cadre non commercial : convenable pour un portfolio, pas pour une vraie diffusion publicitaire. Détail dans [docs/CREDITS.md](docs/CREDITS.md).

## 10. Limites connues
- **Plans IA en 480p agrandis :** image plus douce que les macros. Les ressorts prennent par endroits un aspect « perlé ». La version 1080p demandait environ 400 crédits.
- **Fidélité contrôlée sur images fixes :** sens de l'image, pose et pièces vérifiés plan par plan, mais pas image par image sur toute la durée.
- **Son :** niveau (voix vers −18 dB RMS, crête à −2,8 dBFS) mesuré sans compteur LUFS.
- **Musique coupée :** le morceau Suno dure 60 s ; seules les 31 premières secondes sont utilisées, avec un fondu final.
- **Pas de déclinaison 1:1 ou 9:16** pour les réseaux.
- **Nom TENSIL :** marque fictive, recherche d'antériorité seulement indicative (voir le projet Blender).

## 11. Visuels
| Repos | Tension |
|---|---|
| ![](export/web/01-repos.webp) | ![](export/web/03-tension.webp) |
| **Équilibre** | **Fin** |
| ![](export/web/04-equilibre.webp) | ![](export/web/06-fin.webp) |

**Processus :** [planche des 9 plans](export/web/08-planche-plans.webp) · [préviz Blender contre Seedance](export/web/07-previz-vs-seedance.webp) · [annotation « Ressort »](export/web/02-ressort.webp)

## Documentation
- [Étude de cas](docs/CASE_STUDY.md)
- [Intégration portfolio](docs/PORTFOLIO.md)
- [Fiches Seedance](storyboard/seedance_shots.md)
- [Crédits & licences](docs/CREDITS.md)
- [Coûts](docs/COSTS.md)
- [Suivi des tâches](docs/TODO.md)
