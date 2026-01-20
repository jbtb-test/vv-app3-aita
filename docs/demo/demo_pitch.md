# APP3 — AITA — Pitch entretien (2–3 minutes)

## Contexte

Dans les projets de validation et vérification,
la **conception de tests (test design)** est souvent :

- très manuelle (Excel, Word, ALM),
- fortement dépendante de l’expérience individuelle,
- peu homogène entre projets ou équipes,
- difficile à justifier et à démontrer en audit ou en entretien.

Les exigences existent,
mais la transformation **exigences → cas de test structurés**
reste peu outillée et peu démontrable.

---

## Objectif de l’outil

APP3 — AITA est un **outil de démonstration**
qui outille la **conception de tests** à partir d’exigences.

L’objectif est de :

- structurer le **test design** (aligné ISTQB),
- générer des **cas de test cohérents et justifiables**,
- assurer une **traçabilité explicite exigence → test**,
- produire des **preuves concrètes** exploitables en revue, audit ou entretien.

Les données d’entrée sont des exports simples
issus d’outils comme DOORS, Polarion ou Jira (CSV).

---

## Principe clé

Le cœur de l’outil est **entièrement déterministe**.

- Les cas de test sont générés par une logique explicite
- La structuration est reproductible
- Les résultats sont auditables

L’IA est :
- **désactivée par défaut**
- **strictement non décisionnelle**
- utilisée uniquement pour proposer des **idées de tests complémentaires**
- APP3 — AITA fonctionne **intégralement sans IA**.

---

## Démonstration

À partir d’un fichier CSV d’exigences,
APP3 — AITA génère automatiquement :

- un **pack de cas de test Markdown** (lisible humainement),
- un **pack structuré JSON** (exploitable par outils QA / ALM),
 
(voir `docs/demo/README.md`).

---

## Valeur ajoutée

APP3 — AITA permet :

- une **structuration homogène** du test design,
- une réduction des oublis d’axes de test,
- une traçabilité claire et explicite,
- des preuves immédiatement démontrables,
- une intégration IA maîtrisée, optionnelle et défendable.

---

## Conclusion

APP3 — AITA ne remplace pas
le jugement ni l’expertise de l’ingénieur test.

Il **structure**, **formalise** et **rend démontrable**
la conception de tests.

> Je peux vous montrer soit le pack de tests Markdown/JSON de démonstration, soit l’exécution locale du pipeline, en quelques secondes.

