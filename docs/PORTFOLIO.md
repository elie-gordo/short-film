# Contenu de la page projet (portfolio)

> Le portfolio n'est pas modifié depuis ce dépôt. Ce fichier fournit le texte, les visuels et le bloc prêt à coller dans `Portfolio3.0/src/features/projets/projets.data.ts`.

## Titre
**TENSION — teaser de luxe pour la lampe TENSIL, entre Blender et Seedance**

## Description courte (≈ 300 caractères)
Un teaser de 31 s pour TENSIL, une lampe fictive. Une préviz Blender guide un modèle vidéo IA (Seedance 2.5), les plans macro sont rendus en 3D, le montage et le motion design sont écrits en code, avec une voix off ElevenLabs et une musique Suno. Le film raconte quatre chapitres : repos, tension, équilibre, lumière.

## Place dans le portfolio
TENSIL est présentée sous plusieurs angles : le modèle 3D (Blender), la boutique de démonstration (site), la campagne préparée avec n8n, et ce film. Il réutilise la lampe du projet Blender, la palette et les polices de la boutique, et renvoie vers son adresse dans l'écran de fin.

## Outils utilisés
| Étape | Outil | Usage |
|---|---|---|
| Pilotage | Claude Code (Claude Opus 5.5) | Agent qui écrit et lance les scripts, pilote Blender et Higgsfield, monte le film, écrit les prompts, documente |
| Connexion | Extension Higgsfield pour Blender + MCP `higgsfield-bridge` | Relie Blender à Claude Code |
| Connexion | Connecteur MCP Higgsfield | Envoi des références, devis (`get_cost`), génération, suivi |
| 3D | Blender 5.2.2 LTS, EEVEE, script Python `blender/film.py` | Scène, caméras, animation, préviz, références, 4 plans macro |
| IA vidéo | Seedance 2.5 via Higgsfield, mode `omni_reference` | 5 plans d'ensemble en brouillon 480p |
| Montage | Remotion 4 (React 18, TypeScript) | Timeline, étalonnage, grain, vignettage, ralenti, rendu H.264 + AAC |
| Motion design | Remotion + `@remotion/google-fonts` (Archivo Narrow, Azeret Mono, Inter) | Titres, annotations, chapitres, format cinéma, écran de fin |
| Voix off | ElevenLabs, Voice Design + Eleven v3 | 7 phrases, une par titre |
| Musique | Suno, mode Instrumental (Eleven Music essayé d'abord) | Morceau de 60 s, 31 s utilisées |
| Mixage | Remotion | Voix calées à l'image, musique baissée sous la voix, fondu final |
| Analyse | Python 3.11 + numpy, ffmpeg/ffprobe de Remotion | Choix de l'extrait musical, niveaux sonores, vérification des fichiers |
| Médias web | Python + Pillow, `remotion still` | Images WebP, planche des plans, vidéo muette |
| Versionnage | Git, GitHub | Dépôt public |

## Étapes, dans l'ordre
1. **Cadrage** : relecture des projets TENSIL, trois concepts, choix de « TENSION » (la lampe tient par ses ressorts), storyboard de 11 plans sur 30 s.
2. **Connexion des outils** : connecteur Higgsfield vérifié, extension Blender reliée à Claude Code après activation de l'option « Enable MCP control ».
3. **Préviz Blender** : studio sombre, une caméra par plan, la lampe animée joint par joint sur 900 images à 30 i/s, animatic.
4. **Répartition** : gros plans mécaniques en 3D (l'IA y déforme les ressorts), plans d'ensemble en IA.
5. **Plans macro** : 4 plans rendus en EEVEE.
6. **Références Seedance** : pour chaque plan IA, la vidéo de préviz avec 0,5 s de marge, une image de début, une image de fin, les rendus produit, et un prompt qui interdit le miroir et toute modification de la lampe.
7. **Génération** : devis affiché avant chaque lancement, un plan test (P04, 15 crédits) puis les quatre autres en lot ; 72 crédits au total.
8. **Contrôle** : début, milieu et fin de chaque plan comparés à la préviz.
9. **Montage** dans Remotion : plans calés à l'image près, marges retirées, étalonnage pour raccorder IA et 3D, grain, fin ralentie.
10. **Motion design** : bandes cinéma, barre de chapitres, six titres révélés mot par mot, quatre annotations techniques, lueur à l'allumage ; chaque texte placé dans une zone vide du plan.
11. **Écran de fin** « Tenue par la tension. », plus une version sans écran de fin.
12. **Voix off** : une voix créée avec Voice Design, chaque titre généré en phrase séparée avec Eleven v3, puis calé sur son apparition à l'écran.
13. **Musique** : prompt écrit pour Eleven Music puis adapté à Suno (téléchargement payant chez ElevenLabs) ; extrait de 31 s choisi pour que le sommet tombe sur l'allumage.
14. **Mixage** : musique baissée automatiquement sous chaque phrase, film allongé à 31,5 s pour la dernière phrase ; bruitages synthétisés essayés puis retirés.
15. **Exports et documentation** : master, version sans écran de fin, version web, médias du portfolio, README et étude de cas.

## Intégration dans `Portfolio3.0`
1. Copier les médias de `export/web/` vers `Portfolio3.0/public/media/tensil-film/` :
   `tension-teaser.mp4`, `01-repos.webp`, `02-ressort.webp`, `03-tension.webp`, `05-lumiere.webp`, `07-previz-vs-seedance.webp`, `08-planche-plans.webp` (et `card.webp` si une vignette est utile).
2. Coller le bloc ci-dessous dans `projets.data.ts`, au-dessus de `PROJET_SLOTS`.
3. Remplacer l'emplacement libre `p3` (« Projet 03 ») par l'entrée `TENSIL FILM` donnée plus bas.
4. Pousser ce dépôt sur GitHub pour que le lien `repo` réponde.

```ts
const TENSIL_FILM_MEDIA = '/media/tensil-film'

const TENSIL_FILM: ProjetContenu = {
  nom: 'TENSIL FILM',
  accroche: 'Teaser de luxe de 31 s, entre Blender et IA vidéo',
  monogramme: 'T',
  sections: [
    {
      titre: 'Contexte',
      paragraphes: [
        'La lampe TENSIL avait son modèle 3D, sa boutique et sa campagne sociale. Il lui manquait un film : 30 secondes capables de la faire désirer, dans les codes des grandes marques de luxe.',
        'Le teaser raconte une histoire en quatre chapitres, repos, tension, équilibre, lumière, portée par des titres courts, des annotations techniques et une voix off. TENSIL est une marque fictive : aucun produit n’est vendu.',
      ],
    },
    {
      titre: 'Rôle',
      paragraphes: ['Projet réalisé en duo humain + IA :'],
      points: [
        'moi : concept, storyboard de 11 plans, choix du budget et des versions, ligne de fin, direction du motion design, génération de la voix et de la musique, validation de chaque étape ;',
        'Claude (Claude Code) : scripts Blender, préparation et lancement des générations Seedance, montage, motion design et mixage dans Remotion, prompts voix et musique, contrôles et documentation.',
      ],
    },
    {
      titre: 'Outils',
      points: [
        'Pilotage : Claude Code, relié à Blender et à Higgsfield par MCP.',
        'Préviz et macros : Blender 5.2, EEVEE, script Python, une caméra par plan sur une timeline de 900 images.',
        'IA vidéo : Seedance 2.5 via Higgsfield, guidé par la vidéo de préviz, les images de début et de fin et les rendus produit.',
        'Montage, motion design et mixage : Remotion (React, TypeScript).',
        'Voix off : ElevenLabs (Voice Design, Eleven v3). Musique : Suno, en instrumental.',
        'Analyse et médias web : Python (numpy, Pillow), ffmpeg.',
        'Typographie : Archivo Narrow, Azeret Mono et Inter, reprises de la boutique.',
      ],
    },
    {
      titre: 'Démarche',
      points: [
        'Storyboard de 11 plans, puis préviz Blender : caméras et animation de la lampe fixées image par image.',
        'Répartition : les gros plans mécaniques en 3D, les plans d’ensemble en IA, là où elle apporte le réalisme.',
        'Seedance reçoit la préviz comme référence de mouvement, avec un prompt qui interdit le miroir et toute modification de la lampe.',
        'Un plan test avant les quatre autres, coût affiché avant chaque génération, résultat comparé à la préviz.',
        'Montage et motion design en code : étalonnage, titres mot par mot, annotations, écran de fin.',
        'Voix off générée phrase par phrase et calée sur les titres, musique choisie pour culminer à l’allumage et baissée sous la voix.',
      ],
    },
    {
      titre: 'Résultat',
      paragraphes: ['Un film de 31 s en 1080p avec voix off et musique, pour 72 crédits de génération.'],
      points: [
        'Récit : 4 chapitres, 6 titres, 4 annotations techniques et 7 phrases de voix off.',
        'Production : 4 plans macro en 3D et 5 plans en IA, sur les mêmes caméras et le même timing.',
        'Fidélité : la lampe garde sa forme et son orientation d’un plan à l’autre, vérifiées plan par plan.',
        'Budget : coût affiché avant chaque génération, un plan test avant les quatre autres.',
        'Livrables : master, version sans écran de fin, version web et médias du portfolio.',
      ],
    },
  ],
  etiquettes: {
    domaine: ['Film publicitaire', 'Motion design', 'IA générative', 'Montage son'],
    outils: ['Blender', 'Seedance', 'Higgsfield', 'Remotion', 'ElevenLabs', 'Suno', 'TypeScript', 'Python', 'Claude Code'],
    annee: '2026',
  },
  medias: [
    { type: 'video', src: `${TENSIL_FILM_MEDIA}/tension-teaser.mp4`, alt: 'Teaser de 31 s : la lampe TENSIL au repos, sous tension, puis allumée', legende: 'Le teaser en entier (31 s, sans son)' },
    { src: `${TENSIL_FILM_MEDIA}/05-lumiere.webp`, alt: 'La lampe allumée projette une flaque de lumière, titre « Alors seulement, la lumière. »', legende: 'Chapitre IV : la lumière' },
    { src: `${TENSIL_FILM_MEDIA}/03-tension.webp`, alt: 'Le bras de la lampe se lève, titre « Toute sa force tient dans la retenue. »', legende: 'Chapitre II : la tension' },
    { src: `${TENSIL_FILM_MEDIA}/02-ressort.webp`, alt: 'Gros plan sur un ressort avec une annotation technique', legende: 'Annotation technique sur un plan macro' },
    { src: `${TENSIL_FILM_MEDIA}/01-repos.webp`, alt: 'La lampe pliée au repos, titre « Au repos, jamais inerte. »', legende: 'Chapitre I : le repos' },
    { src: `${TENSIL_FILM_MEDIA}/07-previz-vs-seedance.webp`, alt: 'Même plan en préviz Blender et en résultat Seedance, côte à côte', legende: 'Processus : préviz Blender et résultat IA' },
    { src: `${TENSIL_FILM_MEDIA}/08-planche-plans.webp`, alt: 'Planche des neuf plans du film, du ressort à l’allumage', legende: 'Processus : les 9 plans du film' },
  ],
}
```

Entrée à mettre à la place de `{ id: 'p3', onglet: 'Projet 03', … }` (la couleur reprend celle de l'emplacement) :

```ts
  {
    id: 'p3',
    onglet: 'TENSIL FILM',
    slug: 'short-film',
    couleur: '#ff4fb0',
    encre: '#000',
    repo: 'https://github.com/elie-gordo/short-film',
    contenu: TENSIL_FILM,
  },
```

## Problème
Une IA vidéo produit des images séduisantes, mais elle redessine le produit à chaque plan : bras en plus, ressorts fondus, image inversée. Pour un film de marque, la forme de l'objet n'est pas négociable. Le budget, lui, limitait les générations.

## Solution
- **Préviz d'abord** : chaque caméra et chaque timing sont fixés dans Blender. Seedance reçoit cette vidéo comme référence, plus les images de début et de fin et les rendus produit.
- **Le bon outil par plan** : les gros plans mécaniques sont rendus en 3D, l'IA ne fait que les plans d'ensemble.
- **Un plan test** avant de lancer les autres, avec le coût affiché à chaque fois.
- **Tout le reste en code** : montage, étalonnage, motion design et mixage se reconstruisent en commandes.

## Rôle de l'IA et limites
- Seedance génère 5 plans en brouillon 480p, agrandis au montage : l'image est plus douce que celle des plans 3D.
- Claude Code écrit les scripts, le montage et les prompts ; chaque étape est validée par moi avant la suivante.
- Les annotations (42 spires, laiton tourné) sont inventées pour le récit, comme la marque.
- Voix off (ElevenLabs) et musique (Suno) viennent d'offres gratuites : usage non commercial, suffisant pour un portfolio.

## Coûts
72 crédits Higgsfield sur un plan Plus (prix du plan à reporter dans `docs/COSTS.md`). Blender, Remotion, ElevenLabs et Suno (offres gratuites) ne coûtent rien.

## Compétences démontrées
- Écriture d'un récit publicitaire court et d'un motion design de marque.
- Pilotage d'une IA vidéo par une préviz 3D, avec contrôle de fidélité.
- Orchestration d'un agent IA relié aux outils de création (Blender, Higgsfield) par MCP.
- Montage, étalonnage et mixage reproductibles en code.
- Direction de voix off et de musique générées par IA.
- Gestion d'un budget de génération.
- Cohérence de marque entre quatre projets.

## Chiffres clés
- 31,5 s, 11 plans, 4 chapitres, 7 phrases de voix off, 1080p à 30 i/s.
- 5 plans IA et 4 plans 3D, sur une seule timeline.
- 72 crédits dépensés.

## Visuels
| Ordre | Fichier | Montre |
|---|---|---|
| 1 | `export/web/tension-teaser.mp4` | le film en entier, sans son (2,4 Mo) |
| 2 | `export/web/05-lumiere.webp` | le moment clé : l'allumage |
| 3 | `export/web/03-tension.webp` | un titre du récit sur un plan IA |
| 4 | `export/web/02-ressort.webp` | une annotation technique sur un plan 3D |
| 5 | `export/web/01-repos.webp` | l'ouverture du récit |
| 6 | `export/web/07-previz-vs-seedance.webp` | le processus : préviz contre résultat IA |
| 7 | `export/web/08-planche-plans.webp` | les 9 plans du film |
| — | `export/web/card.webp`, `04-equilibre.webp`, `06-fin.webp` | vignette 1200×675 et images de réserve |

## Liens
- Dépôt : https://github.com/elie-gordo/short-film
- Projets liés : https://github.com/elie-gordo/blender-studio-object · https://github.com/elie-gordo/website-redesign · https://github.com/elie-gordo/creative-workflow-automation
- Film complet avec son : `export/master/TENSION_master_1080p.mp4` (à héberger si une version sonore doit être en ligne)

## Contrôle final (prévu vs produit)
| Livrable prévu | Produit ? | Remarque |
|---|---|---|
| Film d'environ 30 s, 16:9, 1080p | ✅ | `export/master/TENSION_master_1080p.mp4`, 31,5 s |
| Montage rythmé et habillage | ✅ | 11 plans, motion design en 4 chapitres |
| Ambiance sonore | ✅ | voix off ElevenLabs, musique Suno |
| Plans IA fidèles au produit | ✅ | brouillons 480p ; 1080p non générée (budget) |
| Écran de fin de marque | ✅ | « Tenue par la tension. » ; version sans écran de fin aussi livrée |
| Documentation et coûts | ✅ | README, étude de cas, crédits, coûts (prix du plan à compléter) |
| Déclinaison 1:1 ou 9:16 | ❌ | hors périmètre final |
