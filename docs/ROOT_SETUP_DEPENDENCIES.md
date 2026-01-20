# Setup & Dependencies — Notes internes (APP3 — AITA)

## Principes clés

- `pyproject.toml` = **source de vérité**
- runtime minimal, **sans dépendance IA**
- IA **optionnelle** via extra `ai`
- outils de test via extra `dev`
- layout standard `src/`
- installation en mode éditable (`pip install -e`)
- aucun secret versionné

---

## Installation standard (machine vierge)

```powershell
py -3.14 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -U pip

# Installation standard (déterministe, sans IA)
pip install -e ".[dev]"

# Option IA (suggestions uniquement)
pip install -e ".[dev,ai]"

# Exécution de référence
python -m vv_app3_aita.main --input data/inputs/requirements.csv --out-dir data\outputs --verbose

# Tests
pytest -vv
```

---

## Environnement & secrets

- `.env.example` est versionné
- `.env` / `.env.secret` sont **locaux uniquement**
- aucun secret n’est jamais committé
- `.gitignore` protège tous les fichiers sensibles

