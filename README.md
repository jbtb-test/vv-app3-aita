# APP3 — AITA (AI-assisted Test Ideas & Traceability Accelerator)

## Démo en 1 phrase
Outil orienté **test design (ISTQB)** qui génère un **pack de cas de test** (MD/JSON) à partir d’exigences,
avec **IA optionnelle et non décisionnelle** pour suggérer des idées de tests,
et des **outputs démontrables** (pack + rapport) consultables sur GitHub.

**But :** démontrer une démarche de **conception de tests outillée**, alignée ISTQB,
à partir d’exigences, grâce à un **pipeline maîtrisé** :
- analyse déterministe des exigences
- génération structurée de cas de test
- suggestions **optionnelles** via IA
- production d’outputs démontrables (**MD / JSON **)

> IA = **suggestion only** (jamais décisionnelle).  
> L’application fonctionne **sans IA** par défaut.

---

## Problème métier
La conception de tests est souvent :
- très dépendante de l’expérience individuelle
- peu formalisée et difficile à auditer
- réalisée dans des outils hétérogènes (Excel, ALM, texte libre)
- complexe à démontrer en entretien sans **exemples concrets et traçables**

Les exigences sont disponibles,
mais la **transformation en cas de test exploitables** reste peu outillée.

---

## Valeur apportée
- **Test design structuré** : génération de cas de test alignés ISTQB
- **Traçabilité explicite** : chaque test est lié à une exigence source
- **Gouvernance IA maîtrisée** : suggestions uniquement, jamais décisionnelles
- **Démo portfolio** : packs de tests consultables sans exécuter le code

---

## Fonctionnement (pipeline résumé)

1) **Entrées**  
   CSV d’exigences  
   (format proche DOORS / Polarion)

2) **Analyse déterministe**  
   Validation des données, extraction des intentions de test,
   structuration des cas de test

3) **IA (optionnelle)**  
   Suggestions d’**idées de tests complémentaires**  
   (non décisionnelles, aucune création automatique)

4) **Sorties**
   - Pack de tests en Markdown
   - Pack structuré en JSON

> L’IA est **optionnelle**, **non bloquante**, et **n’influence jamais la structure finale**.

---

## Installation (local)

```powershell
python -m venv venv
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -e ".[dev]"
# option IA
pip install -e ".[dev,ai]"
```


## Tests (CI-friendly)
```bash
pytest -vv
```

---

## Quickstart

### Option A — Démo sans exécution (recommandée pour recruteur)

Cette application fournit un **pack de démonstration figé**, consultable directement sur GitHub,
sans installer ni exécuter Python.

Démonstration **clé en main pour recruteur**, sans installer ni exécuter Python.

Ouvrir :
- `docs/demo/README.md`

Accès direct :
- **Sans IA (moteur déterministe)**  
  `docs/demo/assets/outputs_no_ai/`
- **Avec IA (suggestions gouvernées)**  
  `docs/demo/assets/outputs_ai/`

👉 Point d’entrée unique :
- `docs/demo/README.md`

---

### Option B — Reproduire localement (sans IA, recommandé)

Ce mode correspond au fonctionnement nominal de l’outil
(100 % déterministe, IA désactivée).

```powershell
. .\tools\load_env_secret.ps1
$env:ENABLE_AI="0"
python -m vv_app3_aita.main --out-dir data/outputs --verbose
```

Génère automatiquement :
- Pack de tests Markdown
- Pack JSON structuré

---

### Option C — Mode IA (optionnel, avancé)

Copier `.env.example` en `.env.secret` et renseigner les valeurs localement.  
⚠️ Ne jamais committer `.env` / `.env.*` (seul `.env.example` est versionné).

```powershell
. .\tools\load_env_secret.ps1
$env:ENABLE_AI="1"
python -m vv_app3_aita.main --out-dir data/outputs --verbose
```

## Structure du projet

```text
vv-app3-aita/
├─ src/
│  └─ vv_app3_aita/
├─ tests/
├─ data/
│  └─ inputs/
├─ docs/
│  └─ demo/
└─ README.md
```

> Les dépendances et environnements sont gérés via `pyproject.toml`.
> Les fichiers `requirements*.txt` sont fournis à titre informatif et de traçabilité.

---

### Installation

> Les dépendances et environnements sont gérés via `pyproject.toml`.
> Les fichiers `requirements*.txt` sont fournis à titre informatif et de traçabilité.

---

## ⚖️ Usage & licence

Ce dépôt est fourni à des fins de **démonstration et d’évaluation professionnelle** uniquement.

Il ne constitue pas un produit certifié ni un outil industriel prêt à l’emploi.
Les résultats produits doivent être analysés et validés par un humain.

Lorsqu’elle est activée, l’intelligence artificielle intervient **uniquement en tant que moteur de suggestion**.
Aucune décision automatique n’est prise par l’IA.

© 2026 JBTB. Tous droits réservés.  
Voir le fichier [LICENSE](LICENSE) pour les conditions complètes d’utilisation.

