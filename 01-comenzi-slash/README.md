# Comenzi Slash

> **Nivel:** Incepator | **Durata estimata:** 30 min | **Modul:** 01 din 10

[Cuprins](../README.md) | [Modulul urmator: Memorie si CLAUDE.md >>](../02-memorie/README.md)

---

## Ce vei invata

- Ce sunt comenzile slash si cum functioneaza in Claude Code
- Cele mai importante comenzi built-in, organizate pe categorii, si cand sa le folosesti
- Cum sa creezi propriile comenzi personalizate (skills) care automatizeaza workflow-uri repetitive
- Cum sa folosesti argumente, referinte la fisiere si injectare de context dinamic in comenzi
- Diferenta dintre comenzi built-in, skills personalizate si bundled skills

## De ce conteaza

Comenzile slash sunt punctul de intrare in tot ce face Claude Code dincolo de conversatia simpla. Fara ele, interactiunea se reduce la "scriu ce vreau, astept raspunsul" — ceea ce functioneaza, dar nu scaleaza. Cu comenzile slash, transformi orice workflow repetitiv intr-o actiune de o linie.

Gandeste-te asa: daca folosesti Claude Code zilnic si faci code review de trei ori pe saptamana, diferenta intre a scrie de fiecare data "analizeaza PR-ul curent, verifica securitatea, conformitatea cu stilul proiectului si scrie un rezumat" si a scrie `/review-pr` este enorma. Nu doar ca economisesti timp — elimini inconsistenta. Comanda ta personalizata face acelasi lucru, in acelasi mod, de fiecare data.

Comenzile slash sunt si poarta de intrare catre functionalitati mai avansate: skills (modul 05), hooks (modul 06) si plugins (modul 10) se construiesc toate pe aceeasi fundatie. Odata ce intelegi cum functioneaza comenzile, restul se construieste natural.

## Cum functioneaza

### Cele trei tipuri de comenzi

Claude Code are trei categorii de comenzi slash, si intelegerea distinctiei te ajuta sa navighezi mai eficient:

**Comenzi built-in** sunt implementate direct in Claude Code. Cand scrii `/compact`, `/clear` sau `/model`, Claude Code executa o logica interna fixa — nu trimite un prompt catre modelul AI, ci actioneaza direct. Acestea controleaza sesiunea, interfata si configurarea. Sunt aproximativ 50 de comenzi built-in, si le vezi pe toate scriind `/help`.

**Bundled skills** sunt skills care vin preinstalate cu Claude Code. Spre deosebire de comenzile built-in care executa logica fixa, bundled skills sunt bazate pe prompt-uri: dau lui Claude un set detaliat de instructiuni si il lasa sa orchestreze munca folosind tool-urile disponibile. De exemplu, `/simplify` lanseaza trei agenti de review in paralel, le agrega rezultatele si aplica fix-urile. Alte bundled skills: `/batch` (modificari la scara mare), `/debug` (investigare erori), `/loop` (executie repetata la interval), `/claude-api` (referinta API).

**Skills personalizate** (comenzi custom) sunt cele pe care le creezi tu. Un fisier Markdown cu instructiuni, salvat in `.claude/skills/` sau `.claude/commands/`, devine automat o comanda slash. Aceasta este puterea reala — iti construiesti propria biblioteca de automatizari.

### Comenzi built-in — referinta pe categorii

Nu trebuie sa le memorezi pe toate — dar trebuie sa stii ca exista si unde sa le gasesti. Scrie `/` in Claude Code si incepe sa tastezi pentru a filtra. Iata cele mai importante, grupate dupa ce fac:

**Sesiune si context:**

| Comanda | Ce face |
|---------|---------|
| `/clear` | Sterge complet istoria conversatiei si elibereaza contextul. Aliasuri: `/reset`, `/new` |
| `/compact [instructiuni]` | Comprima conversatia pastrand esentialul. Poti adauga focus: `/compact pastreaza doar ce tine de autentificare` |
| `/resume [sesiune]` | Reia o conversatie anterioara. Fara argument, deschide un selector de sesiuni. Alias: `/continue` |
| `/branch [nume]` | Creeaza o ramificatie din conversatia curenta — util cand vrei sa testezi doua abordari diferite. Alias: `/fork` |
| `/rewind` | Revine la un punct anterior din conversatie si/sau din cod. Plasa ta de siguranta. Alias: `/checkpoint` |
| `/context` | Vizualizeaza cat din fereastra de context e ocupata si primesti sugestii de optimizare |
| `/export [fisier]` | Exporta conversatia curenta ca text |

**Model si performanta:**

| Comanda | Ce face |
|---------|---------|
| `/model [model]` | Schimba modelul AI (Opus, Sonnet, Haiku). Schimbarea se aplica imediat |
| `/fast [on\|off]` | Activeaza/dezactiveaza modul rapid (acelasi model, output mai rapid) |
| `/effort [nivel]` | Seteaza nivelul de efort: `low`, `medium`, `high`, `max` (doar Opus). `auto` reseteaza la implicit |
| `/cost` | Afiseaza statisticile de consum ale sesiunii curente |
| `/usage` | Arata limitele planului si statusul rate limit |

**Cod si Git:**

| Comanda | Ce face |
|---------|---------|
| `/diff` | Deschide un viewer interactiv cu modificarile — poti naviga intre diff-ul git curent si diff-urile per turn |
| `/security-review` | Analizeaza modificarile curente pentru vulnerabilitati de securitate |
| `/pr-comments [PR]` | Afiseaza comentariile de pe un PR GitHub. Detecteaza automat PR-ul branch-ului curent |
| `/plan [descriere]` | Intra in plan mode — proiecteaza o implementare fara sa execute nimic |

**Configurare si diagnostic:**

| Comanda | Ce face |
|---------|---------|
| `/init` | Creeaza un `CLAUDE.md` pentru proiect. Cu `CLAUDE_CODE_NEW_INIT=true`, parcurge interactiv si skills, hooks, memorie |
| `/memory` | Editeaza fisierele CLAUDE.md, activeaza/dezactiveaza auto-memory |
| `/permissions` | Vizualizeaza si modifica permisiunile. Alias: `/allowed-tools` |
| `/config` | Deschide interfata de Settings. Alias: `/settings` |
| `/doctor` | Diagnosticheaza instalarea — verifica daca totul functioneaza corect |
| `/hooks` | Vizualizeaza configurarea hooks (vezi Modul 06) |
| `/mcp` | Gestioneaza conexiunile MCP (vezi Modul 07) |

**Altele utile:**

| Comanda | Ce face |
|---------|---------|
| `/add-dir <cale>` | Adauga un director suplimentar in contextul sesiunii |
| `/btw <intrebare>` | Pune o intrebare laterala fara sa o adaugi in conversatie |
| `/copy [N]` | Copiaza ultimul raspuns in clipboard. `/copy 2` copiaza penultimul |
| `/rename [nume]` | Redenumeste sesiunea curenta |
| `/voice` | Activeaza dictarea vocala push-to-talk |
| `/vim` | Comuta intre modul Vim si Normal de editare |
| `/stats` | Vizualizeaza statistici de utilizare, istoric sesiuni si preferinte model |

### Cum creezi o comanda personalizata (skill)

Aici devine interesant. Orice fisier Markdown salvat in locatia potrivita devine automat o comanda slash. Cel mai simplu exemplu:

```bash
# Creeaza directorul (daca nu exista)
mkdir -p .claude/skills/salut

# Creeaza skill-ul
cat > .claude/skills/salut/SKILL.md << 'EOF'
---
name: salut
description: Saluta si arata ora curenta
---

Saluta-ma prietenos si spune-mi cat e ceasul.
EOF
```

Acum scrii `/salut` in Claude Code si primesti un salut cu ora curenta. Simplu — dar principiul e acelasi pentru automatizari complexe.

**Unde salvezi skill-urile determina cine le poate folosi:**

| Locatie | Cale | Disponibilitate |
|---------|------|-----------------|
| Personal | `~/.claude/skills/<nume>/SKILL.md` | In toate proiectele tale |
| Proiect | `.claude/skills/<nume>/SKILL.md` | Doar in acest proiect (se commiteaza in git) |
| Plugin | `<plugin>/skills/<nume>/SKILL.md` | Unde plugin-ul e activat |

**Nota:** fisierele din `.claude/commands/` functioneaza in continuare si sunt echivalente — dar `.claude/skills/` e formatul recomandat pentru ca suporta fisiere auxiliare, frontmatter mai avansat si invocare automata de catre Claude.

### Frontmatter — configurarea avansata a skill-urilor

Frontmatter-ul YAML (blocul dintre `---` de la inceputul fisierului) controleaza comportamentul skill-ului. Toate campurile sunt optionale:

```yaml
---
name: deploy-prod
description: Deployeaza aplicatia in productie
argument-hint: [versiune]
disable-model-invocation: true
allowed-tools: Bash(npm run *), Read
model: opus
context: fork
---

Deployeaza versiunea $ARGUMENTS in productie:
1. Ruleaza suita de teste
2. Fa build-ul aplicatiei
3. Push catre target-ul de deployment
4. Verifica ca deployment-ul a reusit
```

Campurile cele mai importante:

- **`description`** — ce face si cand sa fie folosit. Claude foloseste asta ca sa decida daca sa incarce skill-ul automat
- **`disable-model-invocation: true`** — doar TU poti invoca skill-ul (Claude nu il va activa singur). Esential pentru comenzi cu side effects: deploy, push, send-message
- **`allowed-tools`** — ce unelte poate folosi Claude cand skill-ul e activ, fara sa ceara permisiune
- **`context: fork`** — ruleaza intr-un sub-agent izolat, fara acces la istoria conversatiei
- **`argument-hint`** — arata in autocomplete ce argumente asteapta (ex: `[numar-issue]`)

### Argumente — cum pasezi date catre skill-uri

Variabila `$ARGUMENTS` preia tot ce scrii dupa numele comenzii. Cand scrii `/fix-issue 123`, textul "123" inlocuieste `$ARGUMENTS` in continutul skill-ului:

```yaml
---
name: fix-issue
description: Rezolva un issue GitHub
disable-model-invocation: true
---

Rezolva issue-ul GitHub #$ARGUMENTS respectand conventiile de cod ale proiectului.
```

Pentru argumente multiple, folosesti `$ARGUMENTS[0]`, `$ARGUMENTS[1]` etc. (sau prescurtat `$0`, `$1`):

```yaml
---
name: migreaza
description: Migreaza un component dintr-un framework in altul
---

Migreaza componenta $0 din $1 in $2. Pastreaza comportamentul si testele existente.
```

Rulat ca `/migreaza SearchBar React Vue`, inlocuieste `$0` cu "SearchBar", `$1` cu "React", `$2` cu "Vue".

### Injectare de context dinamic

Sintaxa `` !`comanda` `` executa o comanda shell INAINTE ca skill-ul sa fie trimis catre Claude. Output-ul inlocuieste placeholder-ul — Claude primeste datele reale, nu comanda:

```yaml
---
name: pr-review
description: Analizeaza PR-ul curent
context: fork
---

## Context PR
- Diff: !`gh pr diff`
- Comentarii: !`gh pr view --comments`
- Fisiere modificate: !`gh pr diff --name-only`

## Sarcina
Analizeaza acest PR si identifica probleme de calitate, securitate si conformitate.
```

Cand rulezi `/pr-review`, comenzile `gh` se executa imediat, iar Claude primeste diff-ul real, comentariile reale si lista de fisiere — totul gata de analizat.

### Referinte la fisiere cu @

In continutul unui skill, `@cale/catre/fisier` include automat continutul acelui fisier in prompt. Util cand vrei ca skill-ul sa aiba mereu acces la un fisier de referinta:

```yaml
---
name: conventii
description: Aplica conventiile de cod ale proiectului
---

Verifica codul modificat si asigura-te ca respecta conventiile din:
@CLAUDE.md
@.eslintrc.json
```

## Ghid practic pas cu pas

Hai sa construim o comanda utila de la zero — un `/commit-smart` care analizeaza modificarile si creeaza un commit cu mesaj descriptiv:

**Pasul 1:** Creeaza directorul skill-ului

```bash
mkdir -p .claude/skills/commit-smart
```

**Pasul 2:** Scrie SKILL.md

```markdown
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

**Pasul 3:** Testeaza

```bash
# In Claude Code:
/commit-smart
```

Claude va analiza diff-ul, va propune un mesaj descriptiv si va crea commit-ul — de fiecare data consistent, de fiecare data cu acelasi nivel de calitate.

## Greseli frecvente si cum le eviti

**Greseala: Skill-uri prea vagi.**
Scrii un skill cu "fa code review pe acest cod" si primesti rezultate inconsistente. Solutia: fii specific. Spune exact CE sa verifice (securitate? performanta? stil?), CUM sa raporteze (bullet points? comentarii inline?) si ce CONVENTII sa respecte (referinta la CLAUDE.md sau .eslintrc).

**Greseala: Uiti `disable-model-invocation: true` pe skill-uri cu side effects.**
Claude poate decide singur sa ruleze un skill daca description-ul se potriveste contextului. Daca skill-ul tau face deploy sau trimite mesaje, adauga `disable-model-invocation: true` — altfel Claude ar putea sa il activeze cand nu te astepti.

**Greseala: Folosesti `/compact` prea devreme.**
Contextul comprimat pierde nuante. Daca esti la 5 minute de conversatie si ai loc, nu comprima. Foloseste `/context` ca sa vezi cat ai ocupat si comprima doar cand esti peste 70-80%.

**Greseala: Nu folosesti `/rewind` cand ceva merge prost.**
Daca Claude a facut o modificare gresita, nu incerca sa il corectezi cu "nu, anuleaza ce ai facut". Foloseste `/rewind` — revine la starea anterioara a conversatiei SI a codului. E mult mai curat si mai sigur.

## Exercitii practice

**Exercitiu 1 — Exploreaza comenzile built-in:**
Deschide Claude Code intr-un proiect si scrie `/`. Navigheaza prin lista. Apoi incearca: `/context` (vezi cat context ai), `/cost` (vezi consumul), `/doctor` (verifica instalarea). Scopul: sa stii ce exista, nu sa memorezi.

**Exercitiu 2 — Creeaza un skill simplu:**
Creeaza un skill `/explain` care primeste un path ca argument si explica ce face acel fisier, cu analogii si diagrame ASCII. Salveaza-l in `~/.claude/skills/explain/SKILL.md` (personal — disponibil in toate proiectele). Testeaza-l cu `/explain src/index.ts`.

**Exercitiu 3 — Skill cu context dinamic:**
Creeaza un skill `/git-status` care foloseste `` !`git status` `` si `` !`git log --oneline -5` `` pentru a injecta starea curenta a repo-ului, apoi cere lui Claude un rezumat al starii proiectului si sugestii pentru urmatorul pas. Adauga `disable-model-invocation: true`.

## Recapitulare

Comenzile slash sunt fundamentul interactiunii avansate cu Claude Code. Ai invatat ca exista trei categorii (built-in, bundled skills, personalizate), ca cele built-in controleaza sesiunea si configurarea, ca bundled skills orchestreaza taskuri complexe, si ca skill-urile personalizate iti permit sa automatizezi orice workflow repetitiv. Ai vazut cum se configureaza cu frontmatter, cum se paseaza argumente si cum se injecteaza context dinamic.

In modulul urmator, vei invata cum sa dai lui Claude memorie permanenta prin `CLAUDE.md` — astfel incat skill-urile tale (si tot restul) sa functioneze in contextul specific al proiectului tau, fara sa repeti aceleasi instructiuni la fiecare sesiune.

---

[Cuprins](../README.md) | [Modulul urmator: Memorie si CLAUDE.md >>](../02-memorie/README.md)
