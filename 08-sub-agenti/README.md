# Sub-agenti

> **Nivel:** Intermediar | **Durata estimata:** 1.5 ore | **Modul:** 08 din 10

[<< Modulul anterior: MCP](../07-mcp/README.md) | [Cuprins](../README.md) | [Modulul urmator: Functionalitati Avansate >>](../09-features-avansate/README.md)

---

## Ce vei invata

- Ce sunt sub-agentii si cum se deosebesc de conversatia principala
- Agentii built-in (Explore, Plan, general-purpose) si cand ii foloseste Claude automat
- Cum sa creezi agenti custom cu fisiere Markdown si frontmatter YAML
- Cum sa controlezi tool-urile, modelul, permisiunile si memoria unui sub-agent
- Cum sa combini sub-agentii cu skills, hooks si MCP
- Cand sa folosesti sub-agenti vs. skills vs. conversatia directa

## De ce conteaza

Pana acum ai lucrat intr-o singura fereastra de context — conversatia ta cu Claude. Cand ceri ceva complex ("cerceteaza cum functioneaza modulul de autentificare, apoi refactorizeaza-l"), Claude trebuie sa citeasca fisiere, sa analizeze codul si sa implementeze — totul in acelasi context. Rezultatul: context plin, raspunsuri lente, si informatii de explorare care polueaza conversatia.

Sub-agentii rezolva asta prin delegare. Fiecare sub-agent ruleaza in propria fereastra de context, cu propriul system prompt, propriile tool-uri si propriile permisiuni. Cand Claude intalneste un task care se potriveste unui sub-agent, il delegheaza. Sub-agentul lucreaza independent si returneaza doar rezultatul relevant — restul ramane in contextul lui, nu in al tau.

Gandeste-te la sub-agenti ca la colegi specializati. In loc sa faci tu totul, delegi: "tu cerceteaza, tu scrie teste, tu fa code review". Fiecare lucreaza in spatiul lui, cu tool-urile lui, si iti raporteaza doar concluziile.

Sub-agentii sunt si motorul din spatele bundled skills. Cand `/simplify` spawneaza trei agenti de review in paralel, sau `/batch` creeaza un agent per unitate de lucru in git worktree izolat — tot sub-agenti sunt.

## Cum functioneaza

### Agentii built-in

Claude Code vine cu agenti built-in pe care ii foloseste automat:

**Explore** — agent rapid, read-only, pe modelul Haiku. Optimizat pentru cautare si analiza de codebase. Nu poate modifica fisiere. Claude il foloseste cand trebuie sa inteleaga codul fara sa faca modificari. Specifica un nivel de profunzime: quick, medium, sau very thorough.

**Plan** — agent de cercetare folosit in plan mode. Read-only, mosteneste modelul conversatiei. Cand esti in plan mode si Claude are nevoie de context, il delegheaza lui Plan sa exploreze codebase-ul.

**general-purpose** — agent complet cu acces la toate tool-urile. Mosteneste modelul conversatiei. Claude il foloseste pentru task-uri complexe, multi-pas, care necesita atat explorare cat si modificari.

**Altii**: Bash (comenzi terminal in context separat), Claude Code Guide (Haiku, pentru intrebari despre Claude Code), statusline-setup (Sonnet, pentru configurarea status line-ului).

### Unde definesti agentii custom

| Locatie | Scop | Prioritate |
|---------|------|-----------|
| `--agents` (CLI flag) | Sesiune curenta (nu se salveaza) | 1 (cea mai mare) |
| `.claude/agents/` | Proiectul curent (se commiteaza) | 2 |
| `~/.claude/agents/` | Toate proiectele tale | 3 |
| Plugin `agents/` | Unde plugin-ul e activat | 4 |

Cand mai multi agenti au acelasi nume, locatia cu prioritate mai mare castiga.

### Structura unui agent custom

Un agent e un fisier Markdown cu frontmatter YAML:

```markdown
---
name: code-reviewer
description: Revizuieste codul pentru calitate si best practices. Foloseste proactiv dupa modificari de cod.
tools: Read, Glob, Grep, Bash
model: sonnet
---

Esti un senior code reviewer. Cand esti invocat:
1. Ruleaza git diff pentru a vedea modificarile recente
2. Concentreaza-te pe fisierele modificate
3. Incepe review-ul imediat

Checklist review:
- Codul e clar si lizibil
- Fara cod duplicat
- Error handling adecvat
- Fara secrete expuse
- Input validation implementat

Ofera feedback pe prioritati: Critic > Avertisment > Sugestie.
```

Frontmatter-ul configureaza agentul, body-ul devine system prompt-ul care il ghideaza.

### Campuri de frontmatter

| Camp | Obligatoriu | Ce face |
|------|------------|---------|
| `name` | Da | Identificator unic (lowercase, cratime) |
| `description` | Da | Cand sa fie folosit — Claude decide pe baza asta |
| `tools` | Nu | Tool-uri permise. Daca lipseste, mosteneste totul |
| `disallowedTools` | Nu | Tool-uri interzise (scoase din lista mostenita) |
| `model` | Nu | `sonnet`, `opus`, `haiku`, ID complet, sau `inherit` (default) |
| `permissionMode` | Nu | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| `maxTurns` | Nu | Numar maxim de turn-uri inainte de oprire |
| `skills` | Nu | Skills incarcate in context la startup (continut complet, nu doar referinta) |
| `mcpServers` | Nu | Servere MCP disponibile agentului (referinta sau definitie inline) |
| `hooks` | Nu | Hooks specifice ciclului de viata al agentului |
| `memory` | Nu | Memorie persistenta: `user`, `project`, sau `local` |
| `background` | Nu | `true` = ruleaza mereu in background |
| `effort` | Nu | `low`, `medium`, `high`, `max` |
| `isolation` | Nu | `worktree` = ruleaza intr-un git worktree temporar izolat |
| `initialPrompt` | Nu | Prompt trimis automat la prima rulare (cand agentul e sesiune principala) |

### Controlul tool-urilor

Doua abordari:

**Allowlist cu `tools`** — doar tool-urile listate sunt disponibile:

```yaml
tools: Read, Grep, Glob, Bash
```

**Denylist cu `disallowedTools`** — mosteneste totul MINUS ce e listat:

```yaml
disallowedTools: Write, Edit
```

Daca ambele sunt setate, `disallowedTools` se aplica primul, apoi `tools` filtreaza restul.

Poti restrictiona si ce sub-agenti poate spawna un agent:

```yaml
tools: Agent(worker, researcher), Read, Bash
```

### Executie foreground vs. background

**Foreground** (default) — blocheaza conversatia pana termina. Prompt-urile de permisiuni si intrebarile de clarificare ajung la tine.

**Background** — ruleaza concurrent, tu continui sa lucrezi. Inainte de lansare, Claude cere toate permisiunile necesare anticipat. Daca sub-agentul are nevoie de clarificari in background, acel tool call esueaza dar agentul continua.

Poti muta un task in background oricand cu **Ctrl+B**.

### Memorie persistenta

Campul `memory` da agentului un director persistent intre conversatii:

| Scope | Locatie | Cand |
|-------|---------|------|
| `user` | `~/.claude/agent-memory/<name>/` | Cunostinte valabile peste toate proiectele |
| `project` | `.claude/agent-memory/<name>/` | Cunostinte specifice proiectului, partajabile prin git |
| `local` | `.claude/agent-memory-local/<name>/` | Cunostinte specifice proiectului, fara git |

Cand memoria e activata, agentul primeste instructiuni de a citi si scrie in directorul de memorie. La fiecare sesiune, primele 200 linii din `MEMORY.md` sunt incluse in context.

Pattern eficient: cere-i agentului sa isi consulte memoria inainte de a incepe ("verifica in memorie ce pattern-uri ai gasit inainte") si sa o actualizeze dupa ("salveaza ce ai invatat").

### Preloading skills in sub-agenti

Campul `skills` injecteaza continutul complet al skill-urilor in contextul agentului la startup:

```yaml
---
name: api-developer
description: Implementeaza endpoint-uri API respectand conventiile echipei
skills:
  - api-conventions
  - error-handling-patterns
---

Implementeaza endpoint-uri API. Urmeaza conventiile din skill-urile preincarcate.
```

Sub-agentii NU mostenesc skills din conversatia parinte — trebuie listate explicit.

### MCP servers scoped la sub-agenti

Poti da unui sub-agent acces la servere MCP care nu sunt disponibile in conversatia principala:

```yaml
---
name: browser-tester
description: Testeaza features in browser real cu Playwright
mcpServers:
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  - github
---
```

Serverele inline se conecteaza cand agentul porneste si se deconecteaza cand termina. Referintele string partajeaza conexiunea parintelui.

### Invocare explicita

Trei moduri de a invoca un sub-agent:

**Limbaj natural** — numeste agentul in prompt si Claude decide:

```
Foloseste sub-agentul code-reviewer sa verifice modificarile recente
```

**@-mention** — garanteaza ca acel agent ruleaza:

```
@"code-reviewer (agent)" verifica modificarile din auth/
```

**Sesiune completa** — intreaga sesiune ruleaza ca acel agent:

```bash
claude --agent code-reviewer
```

Cu `--agent`, system prompt-ul agentului inlocuieste system prompt-ul default. CLAUDE.md si memoria de proiect se incarca normal.

## Ghid practic pas cu pas

### Creeaza un agent de code review

**Pasul 1:** Ruleaza `/agents` in Claude Code → Create new agent → Personal.

**Pasul 2:** Descrie-l: "Un agent de code review care scaneaza fisierele si sugereaza imbunatatiri de calitate, securitate si best practices."

**Pasul 3:** Selecteaza tool-uri: doar Read-only tools (fara Write, Edit).

**Pasul 4:** Selecteaza model: Sonnet (echilibru intre capabilitate si viteza).

**Pasul 5:** Salveaza si testeaza:

```
Foloseste sub-agentul code-reviewer sa verifice ultimele modificari
```

### Agent de debugging cu acces complet

Creeaza `~/.claude/agents/debugger.md`:

```markdown
---
name: debugger
description: Specialist debugging pentru erori si test failures. Foloseste proactiv la orice problema.
tools: Read, Edit, Bash, Grep, Glob
---

Esti un expert in debugging. Cand esti invocat:
1. Capteaza mesajul de eroare si stack trace-ul
2. Identifica pasii de reproducere
3. Izoleaza locatia problemei
4. Implementeaza fix-ul minim
5. Verifica solutia

Pentru fiecare problema, ofera:
- Cauza root explicata
- Dovezi care sustin diagnosticul
- Fix de cod specific
- Abordare de testare
- Recomandari de preventie
```

### Agent de baze de date read-only cu hook de validare

```markdown
---
name: db-reader
description: Executa query-uri read-only pe baza de date
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---

Esti un analist de date cu acces read-only. Executa doar query-uri SELECT.
```

Cu `validate-readonly-query.sh` care blocheaza INSERT, UPDATE, DELETE, DROP etc.

## Configurari de referinta

### Agenti via CLI (pentru automatizari)

```bash
claude --agents '{
  "reviewer": {
    "description": "Expert code reviewer",
    "prompt": "Esti un senior code reviewer.",
    "tools": ["Read", "Grep", "Glob"],
    "model": "sonnet"
  },
  "fixer": {
    "description": "Bug fixer specialist",
    "prompt": "Esti un expert in debugging.",
    "tools": ["Read", "Edit", "Bash", "Grep"]
  }
}'
```

### Dezactivarea unor sub-agenti

In settings.json:

```json
{
  "permissions": {
    "deny": ["Agent(Explore)", "Agent(my-custom-agent)"]
  }
}
```

Sau din CLI: `claude --disallowedTools "Agent(Explore)"`.

## Greseli frecvente si cum le eviti

**Greseala: Prea multi sub-agenti rulati in paralel.**
Fiecare sub-agent care termina returneaza rezultate in conversatia principala. 5 agenti cu rezultate detaliate = context plin rapid. Solutia: limiteaza numarul de agenti paraleli. Pentru paralelism sustinut, foloseste agent teams (Modulul 09) care au contexte complet independente.

**Greseala: Descrieri vagi care nu ghideaza delegarea.**
Un agent cu descrierea "ajuta cu codul" nu spune nimic — Claude nu stie cand sa il delege. Solutia: scrie descrieri specifice cu trigger-words: "Foloseste cand...", "Specialist in...", "Proactiv dupa...".

**Greseala: Dai prea multe tool-uri unui agent specializat.**
Un agent de code review cu acces la Write si Edit poate face modificari cand ar trebui doar sa raporteze. Solutia: da-i exact tool-urile de care are nevoie. Read-only pentru review, toate pentru debugging.

**Greseala: Nu folosesti memorie persistenta.**
Un agent de review care incepe de la zero la fiecare sesiune repeta aceleasi descoperiri. Solutia: activeaza `memory: project` si include in prompt instructiuni de a-si consulta si actualiza memoria.

## Exercitii practice

**Exercitiu 1 — Creaza un agent simplu:**
Foloseste `/agents` pentru a crea un agent personal de tip "explainer" — read-only, model Haiku, care explica cod cu analogii. Testeaza-l pe un fisier din proiect.

**Exercitiu 2 — Agent cu restrictii:**
Creeaza un agent `safe-editor` care poate edita fisiere dar are un hook PreToolUse care blocheaza modificarile in `src/core/`. Testeaza ca hook-ul blocheaza corect.

**Exercitiu 3 — Agent cu memorie:**
Creeaza un agent `pattern-detector` cu `memory: project` care analizeaza codul si isi noteaza pattern-uri si anti-pattern-uri gasite. Ruleaza-l de doua ori — la a doua rulare, verifica ca isi consulta memoria anterioara.

## Recapitulare

Sub-agentii sunt asistenti AI specializati care ruleaza in propriul context, cu propriul system prompt, tool-uri si permisiuni. Claude ii foloseste automat (Explore pentru cautare, Plan pentru planificare, general-purpose pentru task-uri complexe) sau le poti crea custom cu fisiere Markdown si frontmatter. Controleaza tool-urile cu `tools`/`disallowedTools`, modelul cu `model`, si comportamentul cu `permissionMode`, `hooks`, `skills` si `mcpServers`. Memorie persistenta (`memory`) permite acumulare de cunostinte intre sesiuni. Sub-agentii nu pot spawna alti sub-agenti — delegarea e la un singur nivel.

In modulul urmator, vei invata functionalitati avansate: plan mode, agent teams, extended thinking, git worktrees, headless mode si alte capabilitati care combina tot ce ai invatat pana acum.

---

[<< Modulul anterior: MCP](../07-mcp/README.md) | [Cuprins](../README.md) | [Modulul urmator: Functionalitati Avansate >>](../09-features-avansate/README.md)
