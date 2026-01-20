# INTERNAL — Validation intégration IA (APP3 — AITA)

Ce document interne décrit et valide l’intégration de l’IA dans **APP3 — AITA (AI-assisted Test Ideas & Traceability Accelerator)**.

## Objectif

Valider que l’intégration IA dans **APP3 — AITA** respecte les principes suivants :

- IA **optionnelle**
- IA **non bloquante**
- IA **non décisionnelle**
- IA **audit-ready**
- IA **désactivable par configuration**

L’IA agit **exclusivement comme assistant de suggestion d’idées de tests**.

Aucun cas de test n’est créé, modifié ou validé automatiquement par l’IA.

---

## Principe d’architecture

L’architecture d’APP3 — AITA repose sur une séparation stricte :

- Pipeline principal **100 % déterministe**
- Test design aligné ISTQB, indépendant de l’IA
- Appel IA **uniquement si `ENABLE_AI=1`**
- Toute erreur IA déclenche un **fallback propre**
- Aucun livrable critique ne dépend de l’IA

L’IA ne peut en aucun cas :
- bloquer l’exécution
- invalider un résultat
- modifier un cas de test existant

---

## Comportement validé (CAS essentiels)

### CAS 0 — Référence (sans IA)
- `ENABLE_AI=0`
- Pipeline déterministe uniquement
- Génération complète :
  - pack de tests Markdown
  - pack JSON

➡️ **Comportement nominal de référence**
➡️ Aucun appel IA

### CAS 1 — IA demandée, clé absente
- `ENABLE_AI=1`
- `OPENAI_API_KEY` absente
- Log explicite côté application
- Fallback automatique vers :
  - liste vide de suggestions

➡️ Pipeline non interrompu  
➡️ Tous les outputs sont générés

### CAS 2 — IA invalide

- `ENABLE_AI=1`
- Clé API invalide ou rejetée
- Exception IA catchée
- Fallback automatique vers :
  - liste vide de suggestions

➡️ Aucun crash  
➡️ Aucun impact sur le test design déterministe

### CAS 3 — IA valide 

- `ENABLE_AI=1`
- Clé API valide
- Appel IA effectué
- Suggestions d’idées de tests produites

Contraintes respectées :
- les cas de test déterministes sont **inchangés**
- les suggestions IA sont **explicitement identifiées**
- aucune décision automatique n’est prise

---

## Règles de sécurité IA

Les règles suivantes sont strictement appliquées dans APP3 — AITA :

- IA **jamais bloquante**
- IA **jamais décisionnelle**
- IA **strictement additive** (suggestions)
- IA **traçable** (contenu identifié comme IA)
- IA **désactivable par environnement**
- IA **séparée du cœur métier**
- Aucun secret versionné (`.env.secret` jamais committé)

---

## Traçabilité et auditabilité

Chaque résultat permet d’identifier clairement :

- ce qui provient du **test design déterministe**
- ce qui provient de **suggestions IA**

Cette séparation garantit :
- auditabilité
- relecture humaine
- justification des décisions de test

---

## Conclusion

L’intégration IA dans **APP3 — AITA** respecte les exigences V&V :

- séparation stricte déterministe / IA
- robustesse en environnement dégradé
- absence de dépendance critique
- gouvernance claire et défendable

> L’IA assiste l’ingénieur test.
> Elle ne décide jamais.

