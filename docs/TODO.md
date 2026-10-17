# TENSION : suivi des tâches

Teaser de 31,5 s en 16:9 pour TENSIL, lampe de bureau fictive créée pour le portfolio. **Livré le 17/10/2026.**

## Fait
- [x] Audit, direction et choix du concept « TENSION ».
- [x] Storyboard de 11 plans, préviz Blender (`blender/film.py`) et animatic.
- [x] Plans macro EEVEE : P02, P03, P06, P09.
- [x] Références Seedance (vidéo, images de début et de fin) pour P04, P05, P07, P08, P10.
- [x] Plugin Higgsfield relié à Blender (option « Enable MCP control » activée).
- [x] Brouillons Seedance 2.5 en 480p des 5 plans IA (72 crédits), vérifiés sur images fixes : pas de miroir, pose conforme.
- [x] Ligne de fin : « Tenue par la tension. ».
- [x] Montage Remotion (`edit/`) : timeline calée sur `film.py`, étalonnage, grain, vignettage, fin ralentie de P10.
- [x] Motion design : récit en 4 chapitres, titres, annotations techniques, format cinéma, barre de chapitres.
- [x] Écran de fin P11 et version sans écran de fin.
- [x] Bruitages procéduraux (`script/sound.py --sfx-only`).
- [x] Voix off ElevenLabs (7 phrases calées sur les titres) et musique Suno (`assets/audio/`), musique baissée sous la voix ; durée portée à 31,5 s.
- [x] Exports : master, version web, image d'aperçu, médias du portfolio (`export/web/`).
- [x] Documentation : README, étude de cas, portfolio, crédits, coûts.

## Reste à faire
- [ ] Reporter dans `docs/COSTS.md` le prix TTC payé pour le plan Higgsfield Plus.
- [ ] Intégrer le projet dans `Portfolio3.0` (voir `docs/PORTFOLIO.md`).

## Pistes facultatives
- Générer les 5 plans IA en 1080p (environ 80 crédits par plan) et relancer `npm run render`.
- P09 : éclairer davantage le bouton ; P02 : couper avant la goupille simplifiée du ressort.
- Déclinaisons 1:1 et 9:16 pour les réseaux.
- Mesurer le niveau sonore avec un vrai compteur LUFS.
