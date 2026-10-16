# TENSION — fiches de génération Seedance 2.5

> Statut : **prêt, rien de généré.** Aucune génération sans coût affiché par le plugin et accord explicite.

Scène : `blender/tensil_film.blend` (construite par `blender/film.py`). Les références vidéo et images sont dans `export/shots/ref/`. Les images produit sont dans `assets/references/`.

## Réglages communs

| Paramètre | Valeur |
|---|---|
| Modèle | `seedance_2_5`, mode `omni_reference` |
| Ratio | 16:9 |
| Audio | `generate_audio: false` (le son est fait à part) |
| Résolution | brouillon 480p (`draft: true`) → version 1080p uniquement pour le brouillon retenu |
| `video_references` | `export/shots/ref/<plan>_ref.mp4` (1280×720, rendu EEVEE de la préviz) |
| `start_image` | `export/shots/ref/<plan>_first.png` |
| `end_image` | `export/shots/ref/<plan>_last.png` (P05, P07, P08, P10) |
| `image_references` | `assets/references/01_hero.png`, `02_profile.png`, `03_detail.png` (+ `04_lit.png` pour P10) |

### Bloc de prompt commun (à placer en tête de chaque prompt)

```
MIRRORING IS FORBIDDEN: never flip the image horizontally. Follow the reference video exactly:
same camera position, camera path, speed and framing, same lamp pose and timing.
The lamp is the TENSIL desk lamp shown in the reference images. Do not add, remove, bend or
redesign any part of it: graphite lacquered steel arms made of twin parallel rods, conical
graphite shade with a thin brass rim, brass pivot caps, exposed steel coil springs running
alongside each arm segment, round weighted graphite base with a small brass knob at the front.
Rigid metal: no wobbling, no stretching rods, no morphing. No people, no hands, no text, no
extra objects. Seamless charcoal studio, almost black, one hard raking light from the left,
a thin rim light from behind on the right. Photoreal product cinematography, subtle film grain.
```

## Plans

| Plan | Durée générée → gardée | Référence (images du master) | Action et prompt spécifique (après le bloc commun) | Risque |
|---|---|---|---|---|
| **P04** | 5 s → 3,5 s | 181–330 | `The lamp rests folded and completely still, its shade low near the floor. The camera dollies in slowly from the front-left. The lamp's shadow lies across the dark floor. Nothing moves except the camera.` | Faible |
| **P05** | 5 s → 4 s | 286–435 | `Low side view. The lower arm lifts from the base pivot in one smooth, controlled mechanical move; the coil springs along it stretch as it rises; the shade still hangs low and follows passively. Camera almost locked, very slight push in.` | **Élevé** : mouvement articulé, tiges et ressorts |
| **P07** | 4 s → 2 s | 466–585 | `Close-up of the lamp head. The shade tips forward and down, overshoots slightly and settles; the brass rim catches a glint of the raking light. Camera almost static.` | Moyen |
| **P08** | 5 s → 4 s | 526–675 | `Wide side profile. The lamp settles into its working pose with a tiny damped bounce of the arms, then stays perfectly still. Very slow push in. The left side of the frame falls into darkness.` | Moyen (ressorts fins en plan large) |
| **P10** | 5 s → 3,5 s (+ fin ralentie) | 706–855 | `Locked-off three-quarter shot. The lamp is off. The bulb inside the shade flickers twice, then switches on with a warm glow; a soft cone of warm light lands on the floor in front of the lamp as an oval pool; the studio light dims so the lamp becomes the main light source. Faint dust visible in the beam.` | Moyen |

La température de couleur de l'ampoule n'est pas spécifiée dans les dépôts. Le prompt dit seulement « chaude », ce qui correspond à la couleur du spot dans le modèle (1,0 / 0,78 / 0,52).

## Contrôle de fidélité (pour chaque résultat)

1. Extraire 3 images : début, milieu, fin. Les poser à côté des mêmes images de la référence (`_first.png`, image du milieu de `_ref.mp4`, `_last.png`).
2. Cocher la liste suivante. Un seul « non » suffit à rejeter le résultat :
   - silhouette et proportions identiques, sans miroir (tête du même côté de l'image) ;
   - 2 tiges parallèles par segment de bras, aucune tige qui plie ;
   - ressorts présents, le long du bras, sans spires fondues ou en plus visibles à la taille d'affichage ;
   - abat-jour conique avec liseré laiton, capuchons laiton aux pivots ;
   - base ronde, pas de pièce inventée, pas de texte ;
   - mouvement rigide (aucune déformation), timing proche de la référence (±0,3 s sur les temps forts).
3. Rejet : on corrige le prompt (une consigne ciblée sur le défaut vu) et on régénère, **au maximum 2 fois par plan**.
4. Toujours rejeté : on utilise le **rendu EEVEE de secours** du plan (`export/shots/final/<plan>/`), même cadrage et même timing.

## Plafond d'essais et de crédits

| Plan | Brouillons 480p max | Versions 1080p |
|---|---|---|
| P04 | 2 | 1 |
| P05 | 3 | 1 |
| P07 | 2 | 1 |
| P08 | 2 | 1 |
| P10 | 2 | 1 |

Estimation, **à remplacer par le coût affiché sur le bouton Generate** :
- brouillons : 53 s × environ 3 crédits/s ≈ 160 crédits ;
- versions 1080p : 24 s × environ 9 à 12 crédits/s ≈ 215 à 290 crédits ;
- **total ≈ 380 à 450 crédits. Plafond proposé : 500 crédits.**

Les taux par seconde sont déduits des pages Higgsfield (Seedance 2.5 : 10 s = 30 crédits en 480p, 70 en 720p, 120 en 1080p ; 8 s en 1080p = 72 crédits). Ces pages se contredisent sur le 1080p. On ne sait pas non plus si la finalisation d'un brouillon est facturée comme une génération 1080p complète.
