# Avant / Après — Test Design assisté

Ce document compare une **conception de tests manuelle classique**
avec une **conception de tests outillée via APP3 AITA**.

L’objectif est d’illustrer :
- les **gains concrets**
- les **limites assumées**
- la **maîtrise humaine conservée**

> Démo consultable : voir `docs/demo/README.md`

---

## Avant — Conception de tests manuelle classique

### Processus typique

1. Lecture manuelle des exigences (DOORS, Polarion, Excel, PDF)
2. Interprétation individuelle par l’ingénieur test
3. Rédaction des cas de test (Excel, Word, ALM)
4. Structuration variable selon la personne ou le projet
5. Relecture manuelle avant revue ou audit

### Avantages

- Expertise humaine complète
- Compréhension fine du système
- Liberté totale dans la conception
- Arbitrage possible sur les cas ambigus

### Limites observées

- ⏱️ Conception longue et peu industrialisée
- ❌ Axes de test oubliés (limites, erreurs, cas négatifs)
- ❌ Structuration hétérogène des cas de test
- ❌ Justification difficile du *pourquoi* d’un test
- ❌ Traçabilité exigence → test parfois implicite
- ❌ Démonstration difficile en audit ou entretien

---

## Après — Test design outillé avec APP3 AITA

### Processus outillé

1. Export CSV des exigences
2. Exécution locale du pipeline APP3 AITA
3. Validation déterministe des exigences
4. Application d’une logique de test design structurée
5. Génération de cas de test alignés ISTQB
6. (Optionnel) Suggestions IA d’idées de tests complémentaires
7. Génération d’outputs structurés (MD + JSON + HTML)
8. Revue humaine et décision

---

### Avantages concrets

- ⚡ Accélération de la conception de tests
- ✔️ Identification systématique des axes de test
- ✔️ Cas de test structurés et homogènes
- ✔️ Traçabilité explicite exigence → test
- ✔️ Preuves concrètes et auditables
- ✔️ Démonstration possible sans exécuter le code

---

### Limites maîtrisées

- Ne remplace pas l’ingénieur test
- Ne décide pas de la suffisance des tests
- Ne valide pas la couverture fonctionnelle
- Ne comprend pas le contexte métier implicite

---

## Rôle de l’IA (optionnelle)

- Désactivée par défaut
- Fournit uniquement :
  - des suggestions d’**idées de tests complémentaires**

L’IA :
- ne crée pas de cas de test automatiquement
- ne modifie pas les cas existants
- ne décide jamais de la pertinence des tests

👉 Elle agit comme **assistant**, jamais comme décideur.

---

## Comparatif synthétique

| Critère | Test design manuel | APP3 AITA |
|------|------------------|-----------|
| Structuration | Variable | Élevée |
| Dépendance à l’expérience | Forte | Réduite |
| Axes de test | Incomplets | Systématiques |
| Traçabilité | Implicite | Explicite |
| Reproductibilité | Faible | Élevée |
| Démonstrabilité | Faible | Forte |
| Décision humaine | Oui | Oui |
| IA décisionnelle | N/A | Non |

---

## Conclusion

APP3 AITA ne remplace pas l’ingénieur test.  
Il **structure**, **sécurise** et **rend démontrable** la conception de tests.

👉 L’ingénieur reste **responsable de la décision**  
👉 L’outil apporte **méthode, cohérence et preuves concrètes**
