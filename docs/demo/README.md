# APP3 AITA — Demo Pack (Recruteur)

Ce dossier contient une **démonstration complète consultable sans exécuter le code**.

Il permet de comparer :
- le mode **déterministe** (référence V&V / test design)
- et le mode **assisté par IA** (suggestion-only, gouverné)

L’objectif est de montrer une **conception de tests structurée**
à partir d’exigences, avec des **preuves concrètes et auditables**.

---

## 1) Inputs (datasets)

Exports représentatifs d’outils de gestion des exigences
(DOORS / Polarion / Jira).

- Exigences : `assets/inputs/requirements.csv`

Ces exigences constituent l’unique entrée du pipeline.

---

## 2) Mode **Sans IA** — test design déterministe (référence)

Conception de tests **sans IA**, 100 % déterministe.

- Rapport HTML : `assets/outputs_no_ai/aita_report.html`
- Pack de tests Markdown : `assets/outputs_no_ai/tests.md`
- Pack structuré JSON : `assets/outputs_no_ai/tests.json`

➡️ Référence V&V : **reproductible, auditable, défendable en audit**.  
➡️ Les cas de test sont générés par une logique **alignée ISTQB**.

---

## 3) Mode **Avec IA** — suggestions gouvernées (optionnel)

Même pipeline que le mode sans IA, avec en plus des
**suggestions d’idées de tests complémentaires**.

- Rapport HTML : `assets/outputs_ai/aita_report.html`
- Pack de tests Markdown : `assets/outputs_ai/tests.md`
- Pack structuré JSON : `assets/outputs_ai/tests.json`
- (optionnel) Suggestions IA : `assets/outputs_ai/ai_suggestions.md`

➡️ L’IA **n’altère pas** les cas de test générés.  
➡️ Elle **propose uniquement**, sans décision automatique.

---

## 4) Screenshots (PNG)

Captures prêtes pour aperçu GitHub :

- Sans IA : `assets/screenshots/no_ai_report.png`
- Avec IA : `assets/screenshots/ai_report.png`

Ces images permettent une **lecture rapide en entretien**
sans ouvrir les fichiers HTML.

---

## 5) Exécution locale (optionnelle) — génération runtime

### Sans IA (déterministe)

```powershell
$env:ENABLE_AI="0"
python -m vv_app3_aita.main --out-dir data/outputs --verbose
```

### Avec IA (optionnel, avancé)
```powershell
. .\tools\load_env_secret.ps1
$env:ENABLE_AI="1"
python -m vv_app3_aita.main --out-dir data/outputs --verbose
```

> ➡️ Scénario 2–3 min : docs/demo_scenario.md