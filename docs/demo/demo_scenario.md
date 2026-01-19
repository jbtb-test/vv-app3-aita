# Scénario de démonstration — APP3 AITA (2–3 minutes)

Ce scénario est conçu pour une **démonstration courte en entretien ou audit**.  
Il montre la valeur de l’outil pour le **test design (conception de tests)** à partir d’exigences,
**sans dépendance à l’IA** (mode par défaut).

---

## Objectif de la démo

- Illustrer une **démarche de test design structurée (ISTQB)**
- Montrer la transformation **exigences → cas de test**
- Montrer des **outputs concrets** (Markdown / JSON / HTML)
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

### ⏱️ 1:00 – 1:45 — Résultats (pack de tests)

Ouvrir les outputs générés :
- Pack de tests **Markdown**
- Pack structuré **JSON**

**Chaque cas de test est explicitement lié à une exigence.  
Les axes de test sont visibles et justifiables.**

C’est un support orienté **revue, audit et entretien**.

---

### ⏱️ 1:45 – 2:30 — Rapport HTML

Ouvrir le rapport HTML localement.

**Ce rapport est lisible sans outil spécifique.  
Il synthétise les exigences analysées et les cas de test générés.**

Points à montrer :
- structuration des cas de test
- traçabilité exigence → test
- lisibilité globale du test design

### ⏱️ 2:30 – 3:00 — Conclusion

---

**L’outil ne prend aucune décision.  
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
