# Skills

> **Nivel:** Intermediar | **Durata estimata:** 1 ora | **Modul:** 05 din 10

[<< Modulul anterior: Referinta CLI](../04-cli/README.md) | [Cuprins](../README.md) | [Modulul urmator: Hooks >>](../06-hooks/README.md)

---

## Ce vei invata

- Cum sa creezi skills personalizate care automatizeaza workflow-uri repetitive
- Ce face fiecare camp din frontmatter si cum le combini pentru comportamente diferite
- Cum sa controlezi cine invoca un skill (tu, Claude, sau amandoi) si de ce conteaza
- Cum sa injectezi context dinamic, argumente si fisiere de referinta in skills
- Cum sa organizezi skills complexe cu fisiere auxiliare si scripturi
- Ce sunt bundled skills si cum le folosesti eficient

## De ce conteaza

Comenzile slash din Modulul 01 ti-au aratat cum sa interactionezi cu Claude Code dincolo de conversatie. Skills sunt urmatorul nivel: in loc sa scrii un prompt lung de fiecare data cand vrei un code review, un deploy, sau o analiza de PR, scrii instructiunile o singura data intr-un fisier SKILL.md si le invoci cu `/skill-name`. E ca diferenta intre a scrie un script Bash si a tasta aceleasi comenzi manual de fiecare data.

Dar skills sunt mai mult decat "prompt-uri salvate". Claude poate decide singur sa le incarce cand sunt relevante — fara sa scrii `/`. Un skill care descrie conventiile API ale proiectului tau se activeaza automat cand Claude lucreaza pe endpoint-uri. Un skill de deploy se activeaza doar cand il invoci tu explicit. Aceasta distinctie — cine invoca si cand — transforma skills din simple scurtaturi in comportamente inteligente care se adapteaza la context.

Skills urmeaza standardul deschis [Agent Skills](https://agentskills.io), ceea ce inseamna ca instructiunile tale pot functiona si cu alte tool-uri AI. Claude Code extinde standardul cu control asupra invocarii, executie in sub-agenti si injectare de context dinamic.

## Cum functioneaza

### Anatomia unui skill

Un skill e un director cu un fisier `SKILL.md` obligatoriu si, optional, fisiere auxiliare:

```
my-skill/
├── SKILL.md           # Instructiuni principale (obligatoriu)
├── template.md        # Template pe care Claude il completeaza
├── examples/
│   └── sample.md      # Exemplu de output asteptat
└── scripts/
    └── validate.sh    # Script pe care Claude il poate executa
```

`SKILL.md` are doua parti: un bloc de **frontmatter YAML** (intre `---`) care configureaza comportamentul, si **continut Markdown** cu instructiunile pe care Claude le urmeaza cand skill-ul e activ.

```yaml
---
name: review-security
description: Analizeaza codul pentru vulnerabilitati de securitate
allowed-tools: Read, Grep, Glob
---

Analizeaza fisierele modificate pentru vulnerabilitati:
1. Verifica input validation pe toate endpoint-urile
2. Cauta SQL injection, XSS, si CSRF
3. Raporteaza fiecare problema cu severitate si fix sugerat
```

### Unde plasezi skills — ierarhia de prioritate

Locatia unui skill determina cine il poate folosi:

| Scop | Cale | Disponibilitate |
|------|------|-----------------|
| Enterprise | Managed settings (configurat de admin) | Toti userii din organizatie |
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` | In toate proiectele tale |
| Proiect | `.claude/skills/<skill-name>/SKILL.md` | Doar in acest proiect (se commiteaza) |
| Plugin | `<plugin>/skills/<skill-name>/SKILL.md` | Unde plugin-ul e activat |

Cand doua skills au acelasi nume, prioritatea e: enterprise > personal > proiect. Plugin skills folosesc namespace (`plugin-name:skill-name`), deci nu pot intra in conflict.

Skills din subdirectoare se descopera automat. Daca lucrezi in `packages/frontend/`, Claude cauta si in `packages/frontend/.claude/skills/`. Asta suporta monorepo-uri unde fiecare pachet are skills proprii.

**Compatibilitate cu `.claude/commands/`:** fisierele din `.claude/commands/` functioneaza in continuare si suporta acelasi frontmatter. Daca un skill si o comanda au acelasi nume, skill-ul are prioritate. Formatul recomandat e `.claude/skills/` pentru ca suporta fisiere auxiliare si organizare pe directoare.

### Frontmatter — toate campurile disponibile

Frontmatter-ul YAML controleaza comportamentul skill-ului. Toate campurile sunt optionale, dar `description` e recomandat:

| Camp | Ce face |
|------|---------|
| `name` | Numele skill-ului (devine `/slash-command`). Daca lipseste, se foloseste numele directorului. Doar litere mici, cifre si cratime, max 64 caractere |
| `description` | Ce face skill-ul si cand sa fie folosit. Claude foloseste asta ca sa decida daca sa il incarce automat. Daca lipseste, se foloseste primul paragraf din continut |
| `argument-hint` | Hint afisat in autocomplete: `[issue-number]` sau `[filename] [format]` |
| `disable-model-invocation` | `true` = doar TU poti invoca skill-ul. Claude nu il activeaza singur. Esential pentru deploy, push, send-message |
| `user-invocable` | `false` = skill-ul nu apare in meniul `/`. Doar Claude il poate folosi. Util pentru knowledge de background |
| `allowed-tools` | Ce tool-uri poate folosi Claude fara sa ceara permisiune cand skill-ul e activ |
| `model` | Modelul AI folosit cand skill-ul e activ |
| `effort` | Nivel de efort: `low`, `medium`, `high`, `max` |
| `context` | `fork` = ruleaza intr-un sub-agent izolat, fara acces la istoria conversatiei |
| `agent` | Ce tip de sub-agent sa foloseasca cand `context: fork` e setat (`Explore`, `Plan`, `general-purpose`, sau un agent custom) |
| `hooks` | Hooks specifice ciclului de viata al skill-ului |
| `paths` | Glob patterns care limiteaza cand skill-ul se activeaza automat. Ex: `src/api/**/*.ts` |
| `shell` | Shell-ul folosit pentru blocurile `!`command``: `bash` (default) sau `powershell` |

### Controlul invocarii — cine activeaza skill-ul

Aceasta e una din cele mai importante decizii de design. Implicit, atat tu cat si Claude puteti invoca orice skill. Doua campuri schimba asta:

**`disable-model-invocation: true`** — doar TU poti invoca skill-ul. Foloseste pentru orice are side effects: deploy, commit, trimitere mesaje, stergere date. Nu vrei ca Claude sa decida singur ca "codul arata gata, hai sa facem deploy".

**`user-invocable: false`** — doar Claude poate invoca skill-ul. Nu apare in meniul `/`. Foloseste pentru knowledge de background: cum functioneaza un sistem legacy, ce conventii respecta un modul. Claude ar trebui sa stie asta cand e relevant, dar `/legacy-system-context` nu e o actiune utila pentru tine.

| Configurare | Tu poti invoca | Claude poate invoca | Cand se incarca in context |
|-------------|---------------|--------------------|-----------------------------|
| (implicit) | Da | Da | Descrierea — mereu; continutul — la invocare |
| `disable-model-invocation: true` | Da | Nu | Descrierea NU e in context |
| `user-invocable: false` | Nu | Da | Descrierea — mereu; continutul — la invocare |

Descrierile skill-urilor sunt incarcate in context ca Claude sa stie ce e disponibil. Daca ai foarte multe skills, pot depasi bugetul de caractere (2% din fereastra de context, fallback 16.000 caractere). Verifica cu `/context` daca apar avertismente despre skills excluse.

### Argumente si substitutii

Variabila `$ARGUMENTS` preia tot ce scrii dupa numele skill-ului:

```yaml
---
name: fix-issue
description: Rezolva un issue GitHub
disable-model-invocation: true
---

Rezolva issue-ul GitHub #$ARGUMENTS respectand conventiile proiectului.
```

`/fix-issue 123` → Claude primeste "Rezolva issue-ul GitHub #123..."

Pentru argumente multiple, `$ARGUMENTS[N]` sau prescurtat `$N`:

```yaml
---
name: migrate
description: Migreaza un component dintr-un framework in altul
---

Migreaza componenta $0 din $1 in $2. Pastreaza comportamentul existent.
```

`/migrate SearchBar React Vue` → `$0` = SearchBar, `$1` = React, `$2` = Vue.

Alte substitutii disponibile:

| Variabila | Ce contine |
|-----------|-----------|
| `$ARGUMENTS` | Toate argumentele pasate |
| `$ARGUMENTS[N]` sau `$N` | Argumentul de pe pozitia N (0-based) |
| `${CLAUDE_SESSION_ID}` | ID-ul sesiunii curente |
| `${CLAUDE_SKILL_DIR}` | Directorul skill-ului (util in `!`command`` pentru a referi scripturi bundled) |

### Injectare de context dinamic

Sintaxa `` !`comanda` `` executa o comanda shell INAINTE ca skill-ul sa ajunga la Claude. Output-ul inlocuieste placeholder-ul — Claude primeste datele reale, nu comanda:

```yaml
---
name: pr-review
description: Analizeaza PR-ul curent
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Context PR
- Diff: !`gh pr diff`
- Comentarii: !`gh pr view --comments`
- Fisiere modificate: !`gh pr diff --name-only`

## Sarcina
Analizeaza acest PR si identifica probleme de calitate si securitate.
```

Cand rulezi `/pr-review`:
1. Comenzile `gh` se executa imediat (pre-procesare)
2. Output-ul lor inlocuieste placeholder-urile
3. Claude primeste prompt-ul complet cu date reale

Asta e pre-procesare, nu ceva ce Claude executa. Claude vede doar rezultatul final.

### Executie in sub-agent cu `context: fork`

Adauga `context: fork` cand vrei ca skill-ul sa ruleze izolat, fara acces la istoria conversatiei. Continutul SKILL.md devine prompt-ul care conduce sub-agentul:

```yaml
---
name: deep-research
description: Cerceteaza un subiect in profunzime
context: fork
agent: Explore
---

Cerceteaza $ARGUMENTS in profunzime:
1. Gaseste fisierele relevante cu Glob si Grep
2. Citeste si analizeaza codul
3. Rezuma descoperirile cu referinte specifice la fisiere
```

Campul `agent` specifica tipul de sub-agent: `Explore` (read-only, optimizat pentru explorare), `Plan` (arhitectura), `general-purpose` (full access), sau un agent custom din `.claude/agents/`.

**Atentie:** `context: fork` are sens doar pentru skills cu instructiuni explicite de task. Daca skill-ul contine doar guidelines ("foloseste aceste conventii API") fara o sarcina, sub-agentul nu va avea ce sa faca.

### Fisiere auxiliare

Pentru skills complexe, pastreaza SKILL.md sub 500 de linii si muta detaliile in fisiere separate:

```
api-reviewer/
├── SKILL.md              # Instructiuni principale + navigare
├── reference.md          # Documentatie API detaliata
├── examples.md           # Exemple de review-uri bune
└── scripts/
    └── check-openapi.sh  # Script de validare
```

Refera fisierele din SKILL.md ca Claude sa stie ce contin si cand sa le incarce:

```markdown
## Resurse aditionale
- Pentru detalii API complete, vezi [reference.md](reference.md)
- Pentru exemple de review-uri, vezi [examples.md](examples.md)
```

Fisierele auxiliare nu se incarca automat — Claude le citeste on-demand cand are nevoie.

### Bundled skills — ce vin preinstalate

Bundled skills vin cu Claude Code si sunt disponibile in fiecare sesiune. Spre deosebire de comenzile built-in care executa logica fixa, bundled skills sunt bazate pe prompt-uri si pot spawna agenti, citi fisiere si se adapta la codebase-ul tau:

| Skill | Ce face |
|-------|---------|
| `/batch <instructiune>` | Orchestreaza modificari la scara mare in paralel. Cerceteaza codebase-ul, descompune munca in 5-30 unitati independente si prezinta un plan. Dupa aprobare, spawneaza un agent per unitate in git worktree izolat. Fiecare agent implementeaza, ruleaza teste si deschide PR. Necesita git |
| `/claude-api` | Incarca referinta API Claude pentru limbajul proiectului (Python, TypeScript, Java etc.) si Agent SDK. Se activeaza automat cand importi `anthropic` sau `@anthropic-ai/sdk` |
| `/debug [descriere]` | Activeaza debug logging si investigheaza probleme citind log-urile sesiunii |
| `/loop [interval] <prompt>` | Ruleaza un prompt repetat la un interval. Util pentru monitoring: `/loop 5m verifica daca deploy-ul s-a terminat` |
| `/simplify [focus]` | Review pe fisierele modificate recent: reuse, calitate, eficienta. Spawneaza 3 agenti de review in paralel, agrega rezultatele si aplica fix-uri |

## Ghid practic pas cu pas

### Construieste un skill de commit inteligent

**Pasul 1:** Creeaza directorul skill-ului:

```bash
mkdir -p .claude/skills/commit-smart
```

**Pasul 2:** Scrie SKILL.md:

```yaml
---
name: commit-smart
description: Analizeaza modificarile si creeaza un commit cu mesaj descriptiv
disable-model-invocation: true
allowed-tools: Bash(git *)
---

Analizeaza modificarile din staging area (git diff --cached) si cele unstaged (git diff).

1. Identifica natura modificarilor (feature, fix, refactor, docs, test)
2. Scrie un mesaj de commit concis dar descriptiv, focusat pe DE CE, nu pe CE
3. Formatul: prima linie max 72 caractere, apoi un rand gol, apoi detalii
4. Creeaza commit-ul

Daca nu exista modificari staged, intreaba-ma ce fisiere sa adaug.
```

**Pasul 3:** Testeaza cu `/commit-smart`.

### Construieste un skill de PR review cu context dinamic

```yaml
---
name: review-pr
description: Code review complet pe PR-ul curent
context: fork
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash(gh *)
---

## Date PR
- Diff complet: !`gh pr diff`
- Descriere: !`gh pr view`
- Fisiere: !`gh pr diff --name-only`

## Instructiuni review
Analizeaza acest PR si raporteaza:

### Securitate
- Input validation, SQL injection, XSS, CSRF

### Calitate cod
- DRY, SOLID, error handling

### Performanta
- N+1 queries, memory leaks, operatii costisitoare in loop-uri

Raporteaza fiecare problema cu: fisier, linie, severitate, fix sugerat.
```

### Skill cu output vizual

Skills pot bundla si rula scripturi in orice limbaj. Un pattern puternic: generarea de fisiere HTML interactive:

```yaml
---
name: visualize-codebase
description: Genereaza o vizualizare interactiva a structurii proiectului
allowed-tools: Bash(python *)
---

Ruleaza scriptul de vizualizare din directorul skill-ului:

```bash
python ${CLAUDE_SKILL_DIR}/scripts/visualize.py .
```

Deschide fisierul HTML generat in browser.
```

Cu un script Python in `scripts/visualize.py`, obtii un tree view interactiv al codebase-ului direct in browser — fara dependente externe.

## Greseli frecvente si cum le eviti

**Greseala: Uiti `disable-model-invocation: true` pe skills cu side effects.**
Claude poate decide singur sa ruleze un skill daca descrierea se potriveste contextului. Daca skill-ul face deploy, trimite mesaje sau sterge date, asta e periculos. Solutia: adauga `disable-model-invocation: true` pe orice skill care modifica stare externa.

**Greseala: Descriere prea vaga sau prea larga.**
Un skill cu descrierea "ajuta cu codul" se activeaza aproape mereu — consumand context inutil. Un skill cu descrierea "analizeaza vulnerabilitati OWASP Top 10 in endpoint-urile REST TypeScript" se activeaza precis cand trebuie. Solutia: scrie descrieri specifice cu keyword-uri pe care le-ai folosi natural in conversatie.

**Greseala: Pui totul intr-un singur SKILL.md imens.**
Un SKILL.md de 1000 de linii incarca tot in context de fiecare data cand skill-ul e invocat. Solutia: pastreaza SKILL.md sub 500 de linii. Muta documentatie detaliata, exemple si referinte in fisiere auxiliare pe care Claude le citeste on-demand.

**Greseala: Folosesti `context: fork` pe skills fara task explicit.**
Un skill care contine doar guidelines ("foloseste aceste conventii") fara o sarcina concreta nu functioneaza cu `context: fork` — sub-agentul primeste regulile dar nu are ce sa faca. Solutia: foloseste `context: fork` doar pe skills care au un task clar (cerceteaza, analizeaza, genereaza). Skills de tip "reference" ar trebui sa ruleze inline.

## Exercitii practice

**Exercitiu 1 — Skill personal simplu:**
Creeaza un skill `/explain` in `~/.claude/skills/explain/SKILL.md` care primeste un path ca argument si explica ce face fisierul respectiv, cu analogii si diagrame ASCII. Testeaza cu `/explain src/index.ts`. Verifica ca apare in lista de skills cu "What skills are available?".

**Exercitiu 2 — Skill de proiect cu context dinamic:**
Creeaza un skill `/status` in `.claude/skills/status/SKILL.md` care injecteaza `!`git status`` si `!`git log --oneline -5`` si cere lui Claude un rezumat al starii proiectului. Adauga `disable-model-invocation: true` si `context: fork`. Testeaza si observa ca sub-agentul nu are acces la istoria conversatiei.

**Exercitiu 3 — Skill cu fisiere auxiliare:**
Extinde skill-ul `/review-pr` cu un fisier `checklist.md` care contine o lista detaliata de verificari de securitate. Refera-l din SKILL.md cu "Pentru checklist-ul complet, vezi [checklist.md](checklist.md)". Observa cum Claude il citeste on-demand doar cand face review pe aspecte de securitate.

## Recapitulare

Skills transforma instructiuni repetitive in automatizari invocabile cu `/skill-name`. Le configurezi cu frontmatter YAML: `disable-model-invocation` controleaza cine le activeaza, `context: fork` le izoleaza in sub-agenti, `allowed-tools` restrictioneaza ce tool-uri sunt disponibile. Suporta argumente cu `$ARGUMENTS`, context dinamic cu `` !`comanda` ``, si fisiere auxiliare pentru skills complexe. Bundled skills (`/batch`, `/simplify`, `/debug`) vin preinstalate si orchestreaza task-uri complexe cu agenti paraleli.

In modulul urmator, vei invata despre hooks — cum sa automatizezi actiuni care se declanseaza la evenimente specifice (inainte de a scrie un fisier, dupa ce ruleaza un tool, la inceputul sesiunii). Hooks completeaza skills: skills sunt ce face Claude cand ii ceri, hooks sunt ce se intampla automat in jurul actiunilor lui Claude.

---

[<< Modulul anterior: Referinta CLI](../04-cli/README.md) | [Cuprins](../README.md) | [Modulul urmator: Hooks >>](../06-hooks/README.md)
