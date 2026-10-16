# TENSION : reste à faire

Teaser de 30 s en 16:9 pour TENSIL, lampe de bureau fictive créée pour le portfolio. État au 16/10/2026, coût engagé : 0 €.

## Fait

- Audit, direction et choix du concept 1 « TENSION » (étapes A et B).
- Storyboard de 11 plans validé (C).
- Scène Blender `blender/tensil_film.blend`, construite par `blender/film.py` : caméras `CAM_P02` à `CAM_P10`, animation de la lampe, éclairage.
- Animatic : `export/animatic/tensil_animatic_blender.mp4`.
- Références Seedance de P04, P05, P07, P08 et P10 dans `export/shots/ref/` (vidéo Workbench, images de début et de fin).
- Plans macro finaux en EEVEE : P02, P03, P06 et P09 (`export/shots/final/*.mp4`).
- Fiches de génération et prompts : `storyboard/seedance_shots.md`.

## 1. Débloquer Higgsfield (bloquant)

- [ ] Ouvrir `blender/tensil_film.blend` dans Blender 5.1 ou plus récent, ouvrir le panneau Higgsfield, puis cliquer sur **Connect** dans « Supercomputer Connection » (même compte que le Bridge).
- [ ] Vérifier la connexion : `get_host_status` doit renvoyer Blender connecté. Il renvoie actuellement `blr:false`.
- [ ] Lire le schéma réel, ce qui ne coûte rien : `bl_list_models({type:"video", include_schema:true})` et `bl_describe_tool` sur la génération vidéo.
- [ ] Vérifier sur cette base :
  - ce que l'onglet Video envoie réellement (viewport, animation de la caméra, références) ;
  - la durée maximale d'un clip ;
  - si le mode brouillon (Draft) est disponible dans le plugin.

## 2. Budget et plan (décision d'Elliott)

- [ ] Choisir un plan Higgsfield. Le compte actuel est gratuit avec 0 crédit. Usage commercial et 1080p en Seedance 2.5 : plan **Plus** au minimum (49 $/mois, ou 39 $/mois en annuel, 1000 crédits, tarifs relevés le 11/09/2026 et à revérifier).
- [ ] Convertir en euros TTC le prix affiché au moment de l'achat. Budget : 200 € pour 5 projets.
- [ ] Aucun achat ni aucune génération sans affichage préalable du coût et accord explicite.

## 3. Générer les plans Seedance (étape D)

Plans P04, P05, P07, P08 et P10. Pour chacun :

- [ ] Choisir la caméra active `CAM_Pxx` et la plage d'images de référence indiquée dans `storyboard/seedance_shots.md`.
- [ ] Préparer le prompt : bloc commun, puis action propre au plan.
- [ ] Estimer le coût sans dépenser (`bl_estimate_generation`, ou lire le coût affiché sur Generate), puis obtenir l'accord.
- [ ] Générer un brouillon en 480p.
- [ ] Contrôler la fidélité avec la liste de contrôle de la fiche : pas d'image inversée en miroir, tiges et ressorts intacts.
- [ ] Faire au plus 2 nouveaux essais par plan (3 pour P05). Si le résultat reste mauvais, passer au rendu EEVEE de secours.
- [ ] Générer en 1080p uniquement la version retenue.
- [ ] Ranger les clips dans `assets/video/`.

Estimation : environ 380 à 450 crédits. Plafond proposé : 500 crédits.

### Solution de secours EEVEE

- [ ] Pour tout plan rejeté, lancer `film.py shot Pxx` en EEVEE à 1080p. Les mêmes caméra et timing que la référence sont conservés (compter environ 3,4 s par image).

## 4. Retouches optionnelles des macros

- [ ] P09 : l'image est sombre et la course du bouton se voit à peine. Éclairer le bouton ou amplifier la course, puis relancer le rendu (environ 3 min).
- [ ] P02 : en fin de plan, la goupille simplifiée du ressort est visible. Couper un peu plus tôt au montage ou la masquer.

## 5. Montage et finition (étape E)

- [ ] Choisir la ligne de fin : « Tenue par la tension. » ou « La tension, puis la lumière. ».
- [ ] Créer l'écran de fin P11 avec Remotion :
  - wordmark TENSIL et « Lampe de bureau articulée » ;
  - « Projet de démonstration — marque fictive » ;
  - tensil-store.vercel.app ;
  - polices Archivo condensé, Azeret Mono et Inter ; palette nuit `#0f0e0d`, papier `#efebe4` et oxyde `#e0714f`.
- [ ] Créer le plan P1 : noir accompagné de son.
- [ ] Monter les plans dans l'ordre P1 à P11 (30 s, 30 images/s), en suivant les durées du storyboard.
- [ ] Étalonner pour harmoniser les plans Seedance et EEVEE : noirs, chaleur de l'ampoule, grain.
- [ ] Préparer le son :
  - bruitages CC0 ou enregistrés soi-même : grincement du ressort, déclic du bouton, bourdonnement de l'ampoule ;
  - musique libre de droits pour un usage commercial (pas de titre Suno généré avec une offre gratuite) ;
  - noter chaque licence dans `docs/CREDITS.md`.
- [ ] Faire le mixage et contrôler le niveau sonore (environ −14 LUFS pour le web).

## 6. Exports et portfolio (étape F)

- [ ] Exporter le master en MP4 H.264, 1920×1080 à 30 images/s.
- [ ] Exporter une version web légère, une image d'aperçu (poster) et, si besoin, une version 1:1 ou 9:16 pour les réseaux.
- [ ] Remplir `docs/COSTS.md` avec les crédits et les euros réellement dépensés.
- [ ] Remplir `docs/CREDITS.md` : outils, licences, musique et sons.
- [ ] Rédiger `docs/CASE_STUDY.md` et `docs/PORTFOLIO.md` : workflow hybride Blender et Seedance, choix faits, limites de l'IA rencontrées.
- [ ] Mentionner partout que TENSIL est une marque fictive, sans présenter le film comme une publicité pour un vrai produit.

## Points ouverts hors périmètre

- Le README et les crédits du site TENSIL mentionnent la police Instrument Serif alors qu'elle n'est pas chargée. Incohérence à corriger dans le dépôt du site, pas ici.
