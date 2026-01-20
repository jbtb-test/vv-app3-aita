# Architecture — APP3 AITA (AI-assisted Test Ideas & Traceability Accelerator)

> Démo recruteur (sans exécuter le code) : voir `docs/demo/README.md`

## 1. Objectif

APP3 AITA est une application de **conception de tests (test design)** à partir
d’exigences (ex. exports DOORS / Polarion), basée sur un **pipeline déterministe**
avec **assistance IA optionnelle et non décisionnelle**.

L’objectif est de :

- transformer des **exigences** en **cas de test structurés**
- appliquer une **démarche de test design alignée ISTQB**
- produire un **pack de tests exploitable** (Markdown / JSON)
- garantir une **traçabilité explicite exigence → test**
- fournir des **preuves auditables** (pack + rapport)
- démontrer une **maîtrise humaine totale** des décisions

APP3 AITA est conçu comme un **outil d’aide à la conception de tests**,
et non comme un générateur automatique de décisions ou de tests validés.

---

## 2. Principes d’architecture

Principes directeurs :

- **Déterminisme prioritaire**
- **Alignement ISTQB (test design)**
- **Traçabilité complète** (exigences → tests)
- **IA strictement optionnelle et suggestion-only**
- **Auditabilité / démonstrabilité**
- **Exécution locale reproductible**

L’architecture privilégie la clarté, la robustesse et la pédagogie,
plutôt que l’automatisation opaque.

---

## 3. Vue d’ensemble du pipeline

L’application suit un **pipeline linéaire**, exécutable en ligne de commande,
inspiré d’une démarche V-cycle (analyse → conception → vérification).

CSV exigences
     |
     v
[ Parser CSV ]
     |
     v
[ Modèles métier ]
     |
     v
[ Validation des exigences ]
     |
     v
[ Test design déterministe ]
     |
     +----------------------+
     |                      |
     v                      v
[ Pack de tests ]     [ IA (optionnelle) ]
     |                      |
     +----------+-----------+
                |
                v
        [ Agrégation ]
                |
                v
        [ Pack Markdown ]
                |
                v
        [ Pack JSON ]
                |
                v
        [ Revue humaine ]

---

## 4. Description des composants

### 4.1 Entrée — CSV exigences

- Fichier CSV standardisé (`data/inputs/requirements.csv`)
- Colonnes documentées (ID, titre, description, criticité, etc.)
- Aucun format propriétaire imposé

Les exigences constituent l’unique source d’entrée.

### 4.2 Parser CSV

- Implémenté dans `main.py`
- Responsabilités :
  - lecture du CSV
  - validation de la structure minimale
  - transformation en objets métier

Aucune logique de test design n’est appliquée à ce stade.

### 4.3 Modèles métier

- Implémentés dans `models.py`
- Représentent :
  - une exigence
  - un cas de test
  - un lien exigence → test

Les modèles sont volontairement simples, explicites et testables.

### 4.4 Validation des exigences (déterministe)

- Vérifications typiques :
  - unicité des IDs
  - champs obligatoires présents
  - cohérence minimale des données

Les exigences invalides sont rejetées avant toute conception de tests.

### 4.5 Test design déterministe (cœur de l’application)

- Implémenté via :
  - `checklist.py` (axes ISTQB déterministes)
  - `generator.py` (génération des cas de test)

- Rôle :
  - analyser l’intention de l’exigence
  - identifier les axes de test (fonctionnel, limites, erreurs, etc.)
  - générer des **cas de test structurés**

Cette étape est :
- 100 % déterministe
- alignée avec une logique ISTQB
- indépendante de toute IA

C’est le **cœur métier** d’APP3.

### 4.6 Assistance IA (optionnelle)

- Implémentée dans `ia_assistant.py`
- Désactivée par défaut
- Rôle strictement limité à :
  - suggérer des **idées de tests complémentaires**

Contraintes fortes :
- aucune création automatique de tests
- aucune modification du pack déterministe
- aucune décision prise par l’IA
- aucune dépendance pour fonctionner

L’IA est un **outil d’inspiration**, jamais une autorité.

### 4.7 Agrégation des résultats

- Centralisation de :
  - cas de test déterministes
  - suggestions IA (si activée)
- Préparation des données pour export

### 4.8 Exports

**Markdown**
- Cas de test lisibles
- Exploitables en revue, entretien, audit

**JSON**
- Structure exploitable par outils QA / ALM
- Base pour automatisation ultérieure

---

## 5. Exécution

Commande principale :
```bash
python -m vv_app3_aita.main --verbose
```

Résultats :
- Pack Markdown de tests
- Pack JSON structuré
- Logs explicites

---

# 6. Non-objectifs (assumés)

APP3 AITA ne vise pas à :
- remplacer un ingénieur test
- générer des tests certifiés automatiquement
- décider de la suffisance des tests
- dépendre d’une IA pour fonctionner

Ces choix sont volontaires et alignés avec une approche industrielle maîtrisée.

---

## 7. Positionnement entretien / audit

APP3 AITA démontre :
- une démarche de **test design structurée**
- une compréhension des principes ISTQB
- une intégration raisonnée de l’IA
- une capacité à produire des preuves concrètes

L’outil est conçu pour être compris en quelques minutes,
sans prérequis techniques.
