# Étude de cas — TENSION, teaser de 31 s

| Rubrique | Contenu |
|---|---|
| Contexte | TENSIL est une lampe de bureau articulée d'une marque fictive, déjà présentée en 3D (Blender), en boutique de démonstration (site) et en campagne sociale (n8n). Il manquait le film : un teaser de marque capable de faire désirer l'objet en 30 s. |
| Objectif | Prouver le montage rythmé, l'habillage, la création d'une ambiance sonore et la livraison d'une production finalisée, avec un récit et une direction digne d'une marque de luxe, dans un budget maîtrisé. |
| Démarche | Une préviz Blender fixe chaque caméra et chaque timing sur une timeline de 900 images. Les plans macro sont rendus directement en EEVEE. Les plans d'ensemble, où l'IA apporte le réalisme, sont générés par Seedance 2.5 à partir de cette préviz : vidéo de référence, images de début et de fin, rendus produit. Un premier brouillon sert de test avant de lancer les autres. Le montage, le motion design et le son sont écrits en code, donc reproductibles. |
| Mon rôle | Concept « TENSION », storyboard, choix du budget (brouillons plutôt que 1080p), ligne de fin, voix off (ElevenLabs) et musique (Suno), direction du motion design, validation de chaque étape. |
| Rôle de l'IA | **Seedance 2.5** génère 5 plans de 4 à 5 s. **Claude (Claude Code)** écrit et exécute les scripts Blender, prépare les références, affiche le coût avant chaque génération, monte le film dans Remotion, écrit le récit et le motion design, synthétise le son et vérifie chaque plan sur des images fixes. |
| Outils | Blender 5.2 (EEVEE), Higgsfield / Seedance 2.5, ElevenLabs (voix off), Suno (musique), Remotion 4 (React, TypeScript), Python (numpy, Pillow), Google Fonts. |
| Difficultés | **Plugin Blender non relié :** l'option « Enable MCP control » était désactivée ; activée par script. **Budget :** la 1080p demandait environ 400 crédits pour 28 disponibles ; le film utilise les brouillons 480p agrandis, harmonisés par l'étalonnage et le grain. **Durée minimale de 4 s :** les plans courts sont générés avec 0,5 s de poignée puis recadrés au montage. **Textes sur l'image :** plusieurs titres touchaient la lampe ; chaque texte est replacé dans une zone vide, vérifiée plan par plan. **Son :** trop faible au premier jet (−25 dB RMS), puis un pic à 0 dBFS après l'encodage AAC ; corrigés par un limiteur doux et une marge de 2 dB. |
| Résultat | Un film de 31,5 s en 1080p avec voix off et musique, une version de 28,5 s sans écran de fin, une version web et un jeu de médias pour le portfolio. Coût : 72 crédits Higgsfield ; voix et musique sur des offres gratuites, à usage non commercial. |

## Ce que je retiens
- La préviz est ce qui rend l'IA vidéo utilisable sur un produit : sans elle, la lampe change de forme d'un plan à l'autre.
- Tester un seul plan avant de lancer les autres limite les dépenses perdues.
- Un récit court et des annotations techniques donnent une valeur perçue que les images seules n'ont pas.
