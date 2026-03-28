# Functionalitati Avansate

> **Nivel:** Avansat | **Durata estimata:** 2 ore | **Modul:** 09 din 10

[<< Modulul anterior: Sub-agenti](../08-sub-agenti/README.md) | [Cuprins](../README.md) | [Modulul urmator: Plugins >>](../10-plugins/README.md)

---

## Ce vei invata

- Cum functioneaza plan mode si cand sa il folosesti pentru analiza sigura
- Ce este extended thinking si cum sa controlezi profunzimea rationamentului
- Cum sa rulezi sesiuni paralele cu git worktrees
- Cum sa folosesti Claude Code headless in scripturi si CI/CD
- Cum sa programezi task-uri recurente cu scheduled tasks si `/loop`
- Cum sa combini toate functionalitatile invatate in workflow-uri complexe

## De ce conteaza

Modulele anterioare ti-au dat bucatile: skills, hooks, MCP, sub-agenti. Acest modul le pune impreuna. Plan mode iti permite sa analizezi un codebase complex fara sa modifici nimic — Claude cerceteaza si propune, tu decizi. Extended thinking da lui Claude spatiu sa gandeasca in profunzime inainte de a raspunde. Git worktrees iti permit sa rulezi mai multi Claude in paralel, fiecare pe propria copie a repo-ului. Headless mode transforma Claude intr-un tool complet programatic pentru CI/CD.

Aceste functionalitati nu sunt "extra" — sunt cele care transforma Claude Code dintr-un asistent conversational intr-o platforma de dezvoltare. Diferenta intre un utilizator intermediar si unul avansat e ca cel avansat stie sa combine plan mode cu sub-agenti, worktrees cu scheduled tasks, si headless mode cu hooks.

## Cum functioneaza

### Plan mode — analiza fara executie

Plan mode instruieste Claude sa creeze un plan prin analiza read-only a codebase-ului. E perfect pentru explorare, planificarea modificarilor complexe, sau code review sigur.

**Cand sa il folosesti:**
- Implementari multi-pas care necesita editari in multe fisiere
- Explorare de codebase cand vrei sa intelegi inainte de a modifica
- Dezvoltare interactiva cand vrei sa iterezi pe directie cu Claude

**Cum il activezi:**

```bash
# La start de sesiune
claude --permission-mode plan

# In timpul unei sesiuni
# Shift+Tab (cicleaza prin moduri: Normal → Auto-Accept → Plan)

# Headless
claude --permission-mode plan -p "Analizeaza sistemul de autentificare"
```

In plan mode, Claude foloseste `AskUserQuestion` ca sa adune cerinte si sa clarifice obiective. Propune un plan pe care il poti refina cu follow-up-uri. Ctrl+G deschide planul in editorul tau default pentru editare directa.

Cand accepti un plan, Claude denumeste automat sesiunea din continutul planului. Apoi poti iesi din plan mode (Shift+Tab) si cere implementarea.

**Configurare ca mod default:**

```json
// .claude/settings.json
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

### Extended thinking — rationament in profunzime

Extended thinking e activat implicit si da lui Claude spatiu sa gandeasca pas cu pas inainte de a raspunde. Rationamentul intern e vizibil in verbose mode (Ctrl+O).

Pe Opus 4.6 si Sonnet 4.6, thinking-ul foloseste **adaptive reasoning**: modelul aloca dinamic tokeni de gandire in functie de nivelul de effort. Nu e un buget fix — Claude decide cat sa gandeasca in functie de complexitatea task-ului.

**Configurare:**

| Metoda | Ce face |
|--------|---------|
| `/effort` sau `/model` | Seteaza nivelul de efort: `low`, `medium`, `high`, `max` |
| "ultrathink" in prompt | Seteaza effort la high pentru acel turn (Opus/Sonnet 4.6) |
| Option+T / Alt+T | Toggle thinking on/off pentru sesiunea curenta |
| `/config` | Toggle global on/off |
| `MAX_THINKING_TOKENS=N` | Limiteaza bugetul de tokeni (pe Opus/Sonnet 4.6, doar `0` dezactiveaza) |

**Cand sa folosesti effort ridicat:**
- Decizii arhitecturale complexe
- Bug-uri dificile de diagnosticat
- Planificare implementare multi-pas
- Evaluarea trade-off-urilor intre abordari diferite

**Atentie:** tokenii de thinking se platesc, chiar daca modelele Claude 4 afiseaza thinking rezumat.

### Git worktrees — sesiuni paralele izolate

Cand lucrezi pe mai multe task-uri simultan, fiecare sesiune Claude are nevoie de propria copie a codebase-ului. Git worktrees rezolva asta creand directoare separate care au propriile fisiere si branch, dar partajeaza acelasi repository history.

```bash
# Creeaza worktree si lanseaza Claude in el
claude --worktree feature-auth

# Alta sesiune in worktree separat
claude --worktree bugfix-123

# Worktree cu nume auto-generat
claude --worktree
```

Worktree-urile se creeaza la `<repo>/.claude/worktrees/<name>` si fac branch din `origin/HEAD`.

**Curatare automata:**
- Fara modificari → worktree si branch se sterg automat
- Cu modificari → Claude te intreaba daca vrei sa pastrezi sau sa stergi

**`.worktreeinclude`** — copiaza fisiere gitignored (`.env`, `.env.local`) in worktree-uri noi:

```text
.env
.env.local
config/secrets.json
```

**Sub-agenti in worktrees:** adauga `isolation: worktree` in frontmatter-ul agentului. Fiecare sub-agent primeste propriul worktree care se curata automat la terminare.

Adauga `.claude/worktrees/` in `.gitignore`.

### Headless mode — Claude programatic

Combinand print mode (`-p`) cu flag-uri de control, Claude devine un tool complet programatic:

```bash
# Code review automat in CI/CD
claude -p "analizeaza diff-ul pentru probleme de securitate" \
  --permission-mode plan \
  --output-format json \
  --max-turns 5 \
  --allowedTools "Read" "Grep" "Glob"

# Generare documentatie batch
for file in src/api/*.ts; do
  claude -p "genereaza JSDoc" < "$file" --output-format text > "${file}.doc"
done

# Multi-turn non-interactiv
claude "analizeaza modulul auth"
claude -c -p "acum implementeaza fix-urile propuse"
claude -c -p "ruleaza testele si fix-uieste erorile"
```

Cu `--output-format stream-json`, fiecare eveniment e un obiect JSON pe o linie — perfect pentru dashboards sau integrari real-time.

### Scheduled tasks — task-uri programate

Patru optiuni pentru task-uri recurente:

| Optiune | Unde ruleaza | Cand |
|---------|-------------|------|
| Cloud scheduled tasks | Infrastructura Anthropic | Task-uri care trebuie sa ruleze si cand PC-ul e oprit |
| Desktop scheduled tasks | Masina ta, via desktop app | Task-uri care au nevoie de acces la fisiere locale |
| GitHub Actions | CI pipeline | Task-uri legate de evenimente repo |
| `/loop [interval] <prompt>` | Sesiunea CLI curenta | Polling rapid cat sesiunea e deschisa |

```
/loop 5m verifica daca deploy-ul s-a terminat
/loop 30m ruleaza testele si raporteaza status-ul
```

Task-urile `/loop` se anuleaza cand iesi din sesiune. Pentru task-uri persistente, foloseste cloud scheduled tasks sau GitHub Actions.

### Agent teams — coordonare multi-agent

Pentru paralelism sustinut cu comunicare intre agenti, agent teams ofera sesiuni complet independente cu task-uri partajate. Fiecare agent are propriul context, propriile tool-uri si poate comunica cu ceilalti.

Spre deosebire de sub-agenti (care ruleaza in sesiunea ta), agent teams ruleaza in sesiuni separate. Sunt ideali pentru:
- Modificari la scara mare cu `/batch`
- Workflow-uri unde mai multi agenti lucreaza simultan pe parti diferite
- Scenarii care depasesc fereastra de context a unui singur agent

### Referinte de fisiere cu @

Sintaxa `@` include instant continut in conversatie:

```
Explica logica din @src/utils/auth.js
Care e structura @src/components?
Arata datele din @github:repos/owner/repo/issues
```

- Cai relative sau absolute
- `@` pe fisier adauga si CLAUDE.md din acel director in context
- `@` pe director arata listing-ul, nu continutul
- `@server:resource` pentru resurse MCP

### Imagini in conversatie

Trei moduri de a include imagini:
1. Drag and drop in fereastra Claude Code
2. Copy + Ctrl+V (nu Cmd+V)
3. Cale catre fisier: "Analizeaza aceasta imagine: /path/to/image.png"

Util pentru: screenshots de erori, mockup-uri UI, diagrame de arhitectura, scheme de baze de date.

## Ghid practic pas cu pas

### Workflow complet: Refactorizare planificata cu worktrees

```bash
# 1. Porneste in plan mode
claude --permission-mode plan

# "Analizeaza modulul de plati si propune o strategie de refactorizare"
# Claude cerceteaza, propune plan, tu rafineazi cu follow-up-uri
# Accepti planul

# 2. Iesi din plan mode (Shift+Tab)
# 3. Creeaza worktree pentru implementare izolata
# "lucreaza intr-un worktree pentru implementare"

# 4. Claude implementeaza in worktree izolat
# 5. Testezi, revizuiesti, mergi branch-ul
```

### CI/CD: Code review automat pe PR-uri

```bash
#!/bin/bash
# .github/workflows/review.yml (simplificat)

DIFF=$(gh pr diff)
echo "$DIFF" | claude -p \
  --append-system-prompt "Esti un code reviewer. Raporteaza: securitate, performanta, stil." \
  --output-format json \
  --max-turns 3 \
  --permission-mode plan \
  --allowedTools "Read" "Grep" "Glob"
```

### Monitoring continuu cu /loop

```
/loop 10m verifica PR-urile deschise pe acest repo si raporteaza status-ul CI
```

## Greseli frecvente si cum le eviti

**Greseala: Stai in plan mode cand vrei sa implementezi.**
Plan mode e read-only — Claude nu poate modifica fisiere. Dupa ce accepti planul, iesi din plan mode cu Shift+Tab inainte de a cere implementarea.

**Greseala: Nu folosesti `ultrathink` pe task-uri complexe.**
Extended thinking implicit aloca tokeni adaptiv, dar pentru probleme deosebit de dificile, "ultrathink" forteaza effort level la high. Solutia: include "ultrathink" in prompt cand ai nevoie de rationament in profunzime.

**Greseala: Rulezi worktrees fara `.worktreeinclude`.**
Worktree-urile sunt checkouts fresh — fisierele `.env` lipsesc. Solutia: creeaza `.worktreeinclude` cu lista fisierelor gitignored necesare.

**Greseala: Headless mode fara `--max-turns` si `--allowedTools`.**
In scripturi, Claude poate intra in loop-uri sau cere permisiuni interactiv. Solutia: seteaza intotdeauna `--max-turns` si `--allowedTools` in automatizari.

## Exercitii practice

**Exercitiu 1 — Plan mode:**
Deschide un proiect complex. Intra in plan mode (`claude --permission-mode plan`). Cere o analiza completa a unui modul. Rafineaza planul cu 2-3 follow-up-uri. Accepta planul si iesi din plan mode. Implementeaza prima parte a planului.

**Exercitiu 2 — Worktrees paralele:**
Lanseaza doua sesiuni Claude in worktrees separate (`claude --worktree task-a` si `claude --worktree task-b`). Fa modificari diferite in fiecare. Verifica ca sunt izolate. Sterge worktree-ul fara modificari si pastreaza-l pe cel cu.

**Exercitiu 3 — Headless pipeline:**
Scrie un script Bash care: (1) ruleaza `claude -p` cu `--output-format json` pe fiecare fisier TypeScript din `src/`, (2) extrage campul `result` cu `jq`, (3) salveaza rezultatele intr-un raport Markdown.

## Recapitulare

Functionalitati avansate combina tot ce ai invatat. Plan mode ofera analiza read-only sigura cu planuri iterative. Extended thinking (si "ultrathink") da lui Claude spatiu sa gandeasca in profunzime. Git worktrees permit sesiuni paralele izolate. Headless mode transforma Claude intr-un tool programatic pentru CI/CD. Scheduled tasks si `/loop` automatizeaza task-uri recurente. Agent teams coordoneaza mai multi agenti in sesiuni independente. Referinte `@` si imagini enrichesc contextul conversatiei.

In ultimul modul, vei invata despre plugins — cum sa impachetezi skills, agenti, hooks si MCP servers intr-un pachet distribuibil pe care il poti partaja cu echipa sau comunitatea.

---

[<< Modulul anterior: Sub-agenti](../08-sub-agenti/README.md) | [Cuprins](../README.md) | [Modulul urmator: Plugins >>](../10-plugins/README.md)
