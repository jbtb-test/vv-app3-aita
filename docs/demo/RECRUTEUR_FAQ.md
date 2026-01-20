# APP3 — AITA — FAQ Recruteur

---

## À quoi sert APP3 — AITA ?

À **outiller et structurer la conception de tests (test design)** à partir
d’exigences, en appliquant une démarche **alignée ISTQB**.

L’outil transforme des exigences en :
- **cas de test structurés**
- **packs de tests exploitables**
- **preuves démontrables** (MD / JSON / HTML)

APP3 AITA ne remplace pas l’ingénieur test :
il **structure** et **rend démontrable** le test design.

---

## Dois-je exécuter le code pour comprendre la démo ?

Non.

Un **pack de démonstration figé** est fourni dans `docs/demo/` :
- rapport HTML
- packs de tests
- captures d’écran

Il est **consultable directement sur GitHub**,
sans installer ni exécuter Python.

---

## L’outil dépend-il d’une IA ?

Non.

- Le mode par défaut est **sans IA**
- Les résultats sont **déterministes et reproductibles**
- L’IA est **strictement optionnelle**

APP3 AITA fonctionne **entièrement sans IA**.

---

## Que fait exactement l’IA ?

Uniquement des **suggestions d’idées de tests complémentaires**.

- Aucune création automatique de cas de test
- Aucune modification des tests générés
- Aucune décision prise par l’IA

➡️ *Suggestion-only, jamais décisionnelle.*

---

## Que se passe-t-il si l’IA est absente ou mal configurée ?

Fallback strict :
- aucune erreur bloquante
- mêmes résultats qu’en mode sans IA
- pipeline entièrement fonctionnel

L’IA n’est **jamais critique** pour l’exécution.

---

## Quels livrables sont produits ?

- Pack de cas de test **Markdown**
- Pack structuré **JSON**
- Rapport **HTML** de synthèse
- (optionnel) Suggestions IA clairement identifiées

Tous les livrables sont exploitables
hors de l’outil (revue, audit, entretien).

---

## Pourquoi c’est pertinent en V&V / test ?

- Structuration homogène du **test design**
- Réduction des oublis d’axes de test
- Traçabilité explicite exigence → test
- Support aux revues et audits
- Démonstration claire des décisions de test

---

## Est-ce un produit industriel ?

Non.

C’est un **démonstrateur V&V / test design** destiné à illustrer :
- une démarche de conception de tests outillée
- une architecture propre et maîtrisée
- une intégration IA responsable et défendable


