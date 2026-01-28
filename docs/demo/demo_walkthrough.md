# APP3 — AITA — Walkthrough de démonstration (2–3 minutes)

## Objectif

Guider une démonstration **claire, reproductible et maîtrisée**
de l’outil **APP3 — AITA**, en contexte entretien ou audit V&V.

Ce walkthrough permet :
- d’adapter la démo au temps disponible,
- de répondre sereinement aux questions,
- d’éviter toute dérive technique inutile.

---

## Étape 1 — Démo sans exécution (recommandée en entretien)

Cette étape montre la valeur de l’outil **sans dépendre de l’environnement**.  
➡️ Elle s’appuie sur le **pack démo figé** dans `docs/demo/assets/`.

### Action

1) **Sans IA (test design déterministe)**
- `assets/outputs_no_ai/tests_pack.md`
- `assets/outputs_no_ai/tests_pack.json`

2) **Avec IA (suggestion-only)**
- `assets/outputs_ai/tests_pack.md`
- `assets/outputs_ai/tests_pack.json`

### À montrer

- exigences d’entrée
- cas de test générés (structuration, lisibilité)
- traçabilité explicite exigence → test
- axes de test couverts (fonctionnel, limites, erreurs)
- statut IA (*disabled* vs *enabled*)

**Les cas de test sont générés par une logique déterministe,
alignée ISTQB, indépendante de l’IA.**

### À éviter

- expliquer l’implémentation technique
- commenter le code
- justifier chaque cas de test individuellement

---

## Étape 2 — Exécution locale (optionnelle)

À utiliser uniquement si l’interlocuteur souhaite voir
le fonctionnement réel du pipeline.

### Commande (sans IA — référence V&V)

```powershell
. .\tools\load_env_secret.ps1
$env:ENABLE_AI="0"
python -m vv_app3_aita.main --out-dir data/outputs --verbose
```

Résultats générés (runtime) :
- pack de tests Markdown
- pack structuré JSON

### À montrer

- rapidité d’exécution
- cohérence entre outputs runtime et pack démo
- stabilité des résultats (déterminisme)

### À éviter

- lire les logs ligne par ligne
- détailler les règles internes de test design

---

## Étape 3 — Exécution locale (optionnelle)

```powershell
. .\tools\load_env_secret.ps1
$env:ENABLE_AI="1"
python -m vv_app3_aita.main --out-dir data/outputs --verbose
```

### À montrer

- suggestions IA clairement identifiées
- cas de test déterministes inchangés
- distinction nette entre :
  - tests générés
  - idées de tests suggérées
  
  > L’IA ne crée ni ne modifie les cas de test.
> Elle suggère, l’humain décide.

---

## Conclusion

APP3 — AITA est un outil :
- orienté **test design**
- déterministe par conception,
- traçable et audit-ready,
- avec une IA **maîtrisée et non décisionnelle**.

👉 L’ingénieur test reste responsable de la décision.  
👉 L’outil apporte structure, cohérence et démonstrabilité.


