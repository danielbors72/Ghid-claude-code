# Memorie si CLAUDE.md

> **Nivel:** Incepator | **Durata estimata:** 45 min | **Modul:** 02 din 10

[<< Modulul anterior: Comenzi Slash](../01-comenzi-slash/README.md) | [Cuprins](../README.md) | [Modulul urmator: Checkpoints >>](../03-checkpoints/README.md)

---

## Ce vei invata

- Cum functioneaza cele doua sisteme de memorie ale lui Claude Code (CLAUDE.md si auto-memory)
- Unde sa plasezi fisierele CLAUDE.md si ce impact are fiecare locatie
- Cum sa scrii instructiuni eficiente pe care Claude le respecta consistent
- Cum sa organizezi regulile pentru proiecte mari cu `.claude/rules/`
- Cum functioneaza auto-memory si cum sa o auditezi

## De ce conteaza

Fiecare sesiune Claude Code incepe cu o fereastra de context goala. Fara memorie, Claude e ca un coleg nou in fiecare dimineata — stie sa programeze, dar nu stie nimic despre proiectul tau, conventiile echipei, fisierele pe care nu trebuie sa le atinga, sau cum preferi sa fie organizat codul. Ii spui aceleasi lucruri de fiecare data, si de fiecare data uita.

CLAUDE.md rezolva asta. E un fisier pe care Claude il citeste automat la inceputul fiecarei sesiuni — regulile jocului, scrise o singura data. Dupa ce il configurezi, Claude stie ca proiectul tau foloseste pnpm nu npm, ca testele se ruleaza cu `pytest`, ca fisierele din `vendor/` nu se modifica niciodata, si ca preferi commit messages in engleza. Nu trebuie sa repeti — stie deja.

Auto-memory completeaza ce CLAUDE.md nu acopera. In timp ce lucrezi, Claude isi noteaza singur lucruri pe care le descopera: cum se face build-ul, ce pattern-uri de debugging functioneaza, ce preferinte ai aratat prin corectii. E ca un caiet de notite pe care colegul tau si-l scrie singur dupa ce lucreaza cu tine cateva zile.

Impreuna, cele doua sisteme transforma Claude Code din "un AI generic care stie sa programeze" in "un asistent care imi cunoaste proiectul". Diferenta e enorma — si se compune cu fiecare sesiune.

## Cum functioneaza

### CLAUDE.md — instructiunile tale permanente

CLAUDE.md este un fisier Markdown pe care Claude il citeste la inceputul fiecarei sesiuni. Scrii in el ce vrei sa stie Claude despre proiectul tau, si el respecta acele instructiuni in tot ce face. Nu e magie — e context. Cu cat instructiunile sunt mai specifice si mai concise, cu atat Claude le urmeaza mai consistent.

Cel mai simplu CLAUDE.md arata asa:

```markdown
# Proiectul Meu

## Structura
- `src/` — codul sursa principal
- `tests/` — teste (Jest)
- `docs/` — documentatie

## Conventii
- TypeScript strict, fara `any`
- Indentare 2 spatii
- Teste obligatorii pentru orice functie noua

## Comenzi
- `npm test` — ruleaza testele
- `npm run build` — face build-ul
- `npm run lint` — verificare cod

## Reguli
- Nu modifica fisierele din `vendor/`
- Commit messages in engleza, prezent simplu
- PR-urile trebuie sa aiba descriere cu ## Summary si ## Test plan
```

Acest fisier e suficient ca Claude sa stie cum sa se comporte in proiectul tau. Dar sistemul e mult mai puternic decat atat.

### Ierarhia locatiilor — de la global la local

CLAUDE.md poate exista in mai multe locatii simultan, fiecare cu un scop diferit. Locatiile mai specifice au prioritate mai mare:

| Scop | Locatie | Ce pui aici | Cine il vede |
|------|---------|-------------|--------------|
| **Politica organizatie** | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) | Standarde de securitate, politici de conformitate | Toti userii din organizatie |
| **Instructiuni proiect** | `./CLAUDE.md` sau `./.claude/CLAUDE.md` | Arhitectura, conventii cod, workflow-uri echipa | Echipa (prin git) |
| **Preferinte personale** | `~/.claude/CLAUDE.md` | Stilul tau de cod, scurtaturi personale | Doar tu (toate proiectele) |

Gandeste-te la asta ca la CSS specificity: regulile globale se aplica peste tot, cele de proiect le pot suprascrie, iar cele personale au ultimul cuvant. Claude Code merge si mai departe — citeste CLAUDE.md din toate directoarele parinte pana la radacina. Daca lucrezi in `foo/bar/`, Claude citeste atat `foo/bar/CLAUDE.md` cat si `foo/CLAUDE.md`.

In plus, CLAUDE.md din subdirectoarele proiectului se incarca automat cand Claude citeste fisiere din acel subdirector. Asta permite configuratie granulara: un `frontend/CLAUDE.md` care se activeaza doar cand Claude lucreaza in frontend.

### Importuri — referinte la alte fisiere

CLAUDE.md poate importa alte fisiere cu sintaxa `@cale/catre/fisier`. Fisierele importate sunt expandate si incarcate in context la pornire, alaturi de CLAUDE.md care le refera:

```markdown
# Proiect

Citeste @README.md pentru overview si @package.json pentru comenzi disponibile.

## Instructiuni
- Workflow Git: @docs/git-instructions.md
- Reguli API: @docs/api-rules.md

## Preferinte personale
- @~/.claude/my-project-prefs.md
```

Importurile suporta cai relative (rezolvate fata de fisierul care le contine) si absolute. Pot fi recursive pana la 5 niveluri de adancime. Prima data cand Claude intalneste importuri externe, iti cere aprobarea.

Un pattern util: daca repo-ul tau are deja un `AGENTS.md` pentru alte tool-uri AI, poti importa acel fisier in CLAUDE.md si adauga instructiuni specifice Claude deasupra:

```markdown
@AGENTS.md

## Claude Code
Foloseste plan mode pentru modificari in `src/billing/`.
```

### Organizarea cu `.claude/rules/` — reguli modulare

Pentru proiecte mari, un singur CLAUDE.md devine greu de gestionat. Directorul `.claude/rules/` permite separarea instructiunilor in fisiere pe topic, fiecare acoperind un singur subiect:

```
proiect/
├── .claude/
│   ├── CLAUDE.md              # Instructiuni principale
│   └── rules/
│       ├── code-style.md      # Conventii de stil
│       ├── testing.md         # Reguli testare
│       ├── security.md        # Cerinte securitate
│       ├── frontend/
│       │   └── react.md       # Reguli specifice React
│       └── backend/
│           └── api-design.md  # Reguli design API
```

Regulile fara frontmatter se incarca la pornire, la fel ca `.claude/CLAUDE.md`. Dar regulile cu **frontmatter `paths`** se incarca doar cand Claude lucreaza cu fisiere care se potrivesc pattern-ului — economisesc context si reduc zgomotul:

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# Reguli API

- Toate endpoint-urile trebuie sa includa validare input
- Foloseste formatul standard de eroare
- Include comentarii OpenAPI
```

Aceasta regula se activeaza DOAR cand Claude citeste fisiere TypeScript din `src/api/`. Pattern-urile suportate:

| Pattern | Se potriveste cu |
|---------|-------------------|
| `**/*.ts` | Toate fisierele TypeScript, orice director |
| `src/**/*` | Toate fisierele din `src/` |
| `*.md` | Fisierele Markdown din radacina proiectului |
| `src/components/*.tsx` | Componentele React dintr-un director specific |
| `src/**/*.{ts,tsx}` | TypeScript si TSX din `src/` |

Regulile din `.claude/rules/` suporta si symlinks — poti pastra un set comun de reguli si le link-uiesti in mai multe proiecte:

```bash
ln -s ~/reguli-comune .claude/rules/shared
```

Exista si reguli personale la nivel de user in `~/.claude/rules/` — se aplica in toate proiectele tale, dar cu prioritate mai mica decat regulile de proiect.

### Auto-memory — Claude isi ia notite singur

Auto-memory este al doilea sistem de memorie. Spre deosebire de CLAUDE.md (pe care il scrii tu), auto-memory este scrisa de Claude pe baza a ceea ce descopera in timp ce lucreaza cu tine: cum se face build-ul, ce pattern-uri de debugging functioneaza, ce preferinte ai demonstrat prin corectii ("nu folosi mock-uri la testele de integrare"), ce comenzi specifice proiectului sunt utile.

**Cum functioneaza tehnic:**

Fiecare proiect are un director de memorie la `~/.claude/projects/<proiect>/memory/`. Structura:

```
~/.claude/projects/<proiect>/memory/
├── MEMORY.md              # Index — incarcat la fiecare sesiune
├── debugging.md           # Notite despre debugging
├── api-conventions.md     # Decizii de design API
└── ...                    # Alte fisiere pe topic
```

La inceputul fiecarei sesiuni, Claude citeste primele 200 de linii (sau 25KB) din `MEMORY.md`. Fisierele pe topic (debugging.md etc.) NU se incarca automat — Claude le citeste on demand cand are nevoie de informatia respectiva.

**Activare/dezactivare:**

Auto-memory e activata implicit (din Claude Code v2.1.59+). O poti controla din `/memory` (toggle interactiv) sau din settings:

```json
{
  "autoMemoryEnabled": false
}
```

**Auditare:** tot ce Claude salveaza e plain Markdown pe care il poti citi, edita sau sterge. Ruleaza `/memory` si selecteaza folderul auto-memory pentru a vedea ce a notat.

**Cand Claude isi ia notite:** nu in fiecare sesiune. Claude decide singur ce merita retinut — informatii care ar fi utile intr-o conversatie viitoare. Cand vezi "Writing memory" sau "Recalled memory" in interfata, Claude tocmai actualizeaza sau citeste din memorie.

### Cum se completeaza cele doua sisteme

| | CLAUDE.md | Auto-memory |
|---|---|---|
| **Cine scrie** | Tu | Claude |
| **Ce contine** | Instructiuni si reguli | Pattern-uri si preferinte descoperite |
| **Scop** | Proiect, user sau organizatie | Per proiect (per working tree) |
| **Se incarca** | Integral la fiecare sesiune | Primele 200 linii / 25KB |
| **Foloseste pentru** | Conventii cod, workflow-uri, arhitectura | Comenzi build, debugging insights, preferinte |

CLAUDE.md e ce vrei TU sa stie Claude. Auto-memory e ce CLAUDE descopera singur ca merita retinut.

## Ghid practic pas cu pas

### Configurarea unui proiect de la zero

**Pasul 1:** Genereaza un CLAUDE.md initial

```bash
# In directorul proiectului, in Claude Code:
/init
```

Claude analizeaza codebase-ul si genereaza un CLAUDE.md cu comenzi de build, conventii descoperite si structura proiectului. E un punct de plecare bun — rafineaza-l cu instructiuni pe care Claude nu le poate descoperi singur.

**Pasul 2:** Adauga instructiuni specifice

Deschide CLAUDE.md (manual sau cu `/memory`) si adauga ce lipseste:

```markdown
## Reguli critice
- NICIODATA nu modifica fisierele din `migrations/` manual — foloseste `npm run migrate:create`
- Testele de integrare necesita Redis local pe portul 6379
- Branch-urile de feature pornesc din `develop`, nu din `main`

## Preferinte stil
- Prefer named exports, nu default exports
- Error handling cu custom error classes, nu string-uri
- Comentarii doar cand logica nu e evidenta — nu comenta codul trivial
```

**Pasul 3:** Adauga reguli path-specific (daca proiectul e mare)

```bash
mkdir -p .claude/rules
```

Creeaza `.claude/rules/frontend.md`:

```markdown
---
paths:
  - "src/components/**/*.tsx"
  - "src/hooks/**/*.ts"
---

# Reguli Frontend

- Componentele folosesc functional components cu hooks
- Fiecare component exporta props type separat
- Stilurile cu CSS Modules, nu inline styles
- Testele cu React Testing Library, nu Enzyme
```

**Pasul 4:** Adauga preferinte personale (optionale, nu se commiteaza)

```bash
mkdir -p ~/.claude/rules
```

Creeaza `~/.claude/rules/preferences.md`:

```markdown
# Preferintele mele

- Raspunde in romana cand explic ce vreau
- Commit messages in engleza
- Prefer explicatii detaliate la code review
- Cand creezi fisiere noi, intreaba-ma inainte
```

## Greseli frecvente si cum le eviti

**Greseala: CLAUDE.md prea lung si prea vag.**
Un CLAUDE.md de 500 de linii cu instructiuni generice ("scrie cod bun") consuma context fara sa aduca valoare. Claude il citeste, dar nu stie ce sa priorizeze. Solutia: tinteste sub 200 de linii per CLAUDE.md. Muta detaliile in `.claude/rules/` sau in fisiere importate cu `@`. Scrie instructiuni concrete: "indentare 2 spatii" nu "formateaza codul frumos".

**Greseala: Instructiuni contradictorii intre fisiere.**
Daca CLAUDE.md zice "foloseste Jest" si `.claude/rules/testing.md` zice "foloseste Vitest", Claude alege arbitrar. Solutia: revizuieste periodic toate fisierele de instructiuni. Ruleaza `/memory` ca sa vezi exact ce fisiere se incarca si verifica ca nu se bat cap in cap.

**Greseala: Crezi ca instructiunile din conversatie persista.**
Daca ii spui lui Claude "de acum incolo foloseste pnpm" intr-o conversatie, informatia se pierde la urmatoarea sesiune. Si dupa `/compact`, instructiunile date in conversatie se pot pierde. Solutia: orice vrei sa persiste, pune in CLAUDE.md. Conversatia e efemera — CLAUDE.md e permanent.

**Greseala: Ignori auto-memory.**
Claude isi ia notite, dar nu le verifici niciodata. Poate a salvat ceva gresit sau outdated. Solutia: ruleaza `/memory` periodic si verifica ce a notat Claude. Editeaza sau sterge ce nu mai e relevant — totul e plain Markdown.

## Exercitii practice

**Exercitiu 1 — Creeaza CLAUDE.md pentru un proiect existent:**
Alege un proiect pe care il cunosti bine. Ruleaza `/init` si lasa Claude sa genereze un draft. Apoi editeaza-l manual: adauga 3-5 reguli specifice pe care Claude nu le-ar putea descoperi singur (ex: "branch-urile de release au prefixul `release/`", "API-ul extern nu suporta mai mult de 100 req/min").

**Exercitiu 2 — Creeaza o regula path-specific:**
In acelasi proiect, creeaza un fisier in `.claude/rules/` cu frontmatter `paths` care se aplica doar pe un subdirector. Testeaza ca regula se activeaza cand lucrezi in acel subdirector si nu se incarca altfel (verifica cu `/memory`).

**Exercitiu 3 — Verifica auto-memory:**
Lucreaza 2-3 sesiuni in acelasi proiect, facand corectii explicite ("nu, foloseste `async/await` nu `.then()`"). Dupa a treia sesiune, ruleaza `/memory` si verifica daca Claude a retinut corectiile tale in auto-memory.

## Recapitulare

Ai invatat ca Claude Code are doua sisteme de memorie complementare: CLAUDE.md (instructiuni scrise de tine) si auto-memory (notite pe care Claude si le ia singur). CLAUDE.md suporta o ierarhie de locatii (organizatie > proiect > personal), poate importa alte fisiere, si poate fi organizat in reguli modulare cu `.claude/rules/`. Auto-memory acumuleaza cunostinte intre sesiuni fara efort manual. Impreuna, transforma fiecare sesiune Claude Code din "conversatie cu un AI generic" in "lucru cu un asistent care iti cunoaste proiectul".

In modulul urmator, vei invata despre checkpoints — cum sa salvezi starea sesiunii si sa faci rewind cand ceva nu merge cum trebuie. E plasa de siguranta care iti da curajul sa experimentezi liber.

---

[<< Modulul anterior: Comenzi Slash](../01-comenzi-slash/README.md) | [Cuprins](../README.md) | [Modulul urmator: Checkpoints >>](../03-checkpoints/README.md)
