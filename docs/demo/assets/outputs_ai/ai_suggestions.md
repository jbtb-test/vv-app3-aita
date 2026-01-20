# AI Suggestions — APP3 AITA (snapshot)

Ce fichier met en évidence **uniquement** les apports IA du snapshot de démo.

## Règles IA (gouvernance)
- IA **optionnelle**
- IA = **suggestion-only**
- IA **non bloquante** (fallback si clé absente)
- Les exigences **ne sont jamais modifiées**

## Snapshot summary
- Baseline (no AI): `../outputs_no_ai/tests.md` + `tests.json`
- With AI: `./tests.md` + `tests.json`
- Delta observé : **+4 tests** (1 suggestion IA par exigence)

## Suggestions IA (liste)

> Extraites depuis `outputs_ai/tests.md` — uniquement les idées **Origin: AI**.
> Ces suggestions complètent la checklist ISTQB, sans modifier les exigences.

### REQ-AITA-001
- Idea ID: `REQ-AITA-001-AI-1`
- Description: IA-suggested edge case scenario  
  Requirement excerpt: Le système doit permettre à un utilisateur autorisé de s’authentifier à l’aide d’un identifiant et d’un mot de passe valides.

### REQ-AITA-002
- Idea ID: `REQ-AITA-002-AI-1`
- Description: IA-suggested edge case scenario  
  Requirement excerpt: Le système doit refuser l’accès si l’identifiant ou le mot de passe est incorrect.

### REQ-AITA-003
- Idea ID: `REQ-AITA-003-AI-1`
- Description: IA-suggested edge case scenario  
  Requirement excerpt: Après 5 tentatives d’authentification échouées consécutives, le compte utilisateur doit être temporairement verrouillé.

### REQ-AITA-004
- Idea ID: `REQ-AITA-004-AI-1`
- Description: IA-suggested edge case scenario  
  Requirement excerpt: Chaque tentative d’authentification (réussie ou échouée) doit être journalisée avec l’identifiant utilisateur et l’horodatage.

