# Scénario de démonstration — APP3 AITA (2–3 minutes)

Ce scénario est conçu pour une **démonstration courte en entretien ou audit**.  
Il montre la valeur de l’outil pour le **test design (conception de tests)** à partir d’exigences,
**sans dépendance à l’IA** (mode par défaut).

---

## Objectif de la démo

- Illustrer une **démarche de test design structurée (ISTQB)**
- Montrer la transformation **exigences → cas de test**
- Montrer des **outputs concrets** (Markdown / JSON )
- Insister sur la **maîtrise humaine** et la **non-décision IA**

---

## Pré-requis (avant entretien)

- Repository cloné
- Environnement Python prêt
- Fichier :
  - `data/inputs/requirements.csv`
- IA désactivée (`ENABLE_AI=0`)

---

## Script chronométré

### ⏱️ 0:00 – 0:30 — Contexte

> « Je pars d’un export d’exigences, typiquement issu de DOORS ou Polarion.
> La conception de tests reste souvent très manuelle, dépendante de l’expérience, 
> et difficile à démontrer. »

> « L’objectif ici est de **structurer le test design** et de produire des **preuves concrètes et auditables**. »

*(Aucune manipulation à l’écran)*

---

### ⏱️ 0:30 – 1:00 — Lancement du pipeline

Commande exécutée :

```bash
python -m vv_app3_aita.main --verbose
```

---

### ⏱️ 1:00 – 2:30 — Résultats (pack de tests)

1. **Baseline**
   - Ouvrir `assets/outputs_no_ai/tests.md`
   - Expliquer la génération via checklist ISTQB.

2. **IA en complément**
   - Ouvrir `assets/outputs_ai/tests.md`
   - Montrer les tests supplémentaires taggés IA.

3. **Gouvernance**
   - Ouvrir `assets/outputs_ai/ai_suggestions.md`
   - Insister sur “suggestion-only”, traçabilité, non-blocage.

---

### ⏱️ 2:30 – 3:00 — Conclusion

---

**L’outil ne prend aucune décision.
L’IA **augmente la couverture** sans jamais prendre de décision.
Il structure, formalise et rend démontrable le test design.**

Optionnel :

**L’IA peut être activée uniquement pour suggérer des idées de tests complémentaires,
sans créer ni modifier automatiquement les cas de test.**

APP3 AITA est un outil de **conception de tests** :
- déterministe
- structuré
- démontrable
- défendable en audit

**L’ingénieur test reste au centre de la décision.**
