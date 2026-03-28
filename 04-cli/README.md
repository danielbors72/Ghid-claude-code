# Referinta CLI

> **Nivel:** Incepator | **Durata estimata:** 30 min | **Modul:** 04 din 10

[<< Modulul anterior: Checkpoints](../03-checkpoints/README.md) | [Cuprins](../README.md) | [Modulul urmator: Skills >>](../05-skills/README.md)

---

## Ce vei invata

- Cum sa lansezi Claude Code in diferite moduri: interactiv, one-shot, print mode, headless
- Ce flag-uri controleaza comportamentul sesiunii si cum sa le combini
- Cum sa integrezi Claude Code in scripturi, pipe-uri si automatizari
- Cum sa gestionezi modelele, permisiunile si configurarea din linia de comanda
- Comenzi de administrare: update, autentificare, MCP, plugins

## De ce conteaza

Cei mai multi utilizatori lanseaza Claude Code cu `claude` si lucreaza interactiv. E suficient pentru 80% din cazuri — dar CLI-ul ofera mult mai mult. Print mode (`-p`) transforma Claude intr-un tool de linie de comanda pe care il poti pune in pipe-uri, scripturi si automatizari CI/CD. Continuation mode (`-c`) te readuce exact unde ai ramas fara sa cauti sesiuni vechi. Flag-urile de system prompt iti permit sa controlezi comportamentul lui Claude fara sa modifici CLAUDE.md.

Diferenta intre un utilizator care stie doar `claude` si unul care stie sa combine `-p`, `--output-format`, `--allowedTools` si pipe-uri shell e ca diferenta intre cineva care stie sa deschida un terminal si cineva care stie sa scrie scripturi Bash. Amandoi folosesc acelasi tool — dar unul il foloseste la o fractiune din capacitate.

## Cum functioneaza

### Moduri de lansare

Claude Code are patru moduri principale de lansare, fiecare cu un scop diferit:

**Modul interactiv** — cel standard. Scrii `claude` si intri intr-o sesiune de conversatie. Ai acces la toate comenzile slash, la checkpoints, la rewind. E modul in care lucrezi zi de zi.

```bash
claude                        # Sesiune noua in directorul curent
claude "refactorizeaza auth"  # Sesiune noua cu un prompt initial
```

Cand pasezi un argument text direct (fara flag), Claude deschide o sesiune interactiva si trimite acel text ca prim mesaj. Diferenta fata de print mode: sesiunea ramane deschisa si poti continua conversatia.

**Print mode (`-p`)** — Claude raspunde si iese. Nu deschide sesiune interactiva, nu salveaza istoric. E perfect pentru scripturi si pipe-uri:

```bash
claude -p "explica ce face acest fisier" < src/auth.ts
cat error.log | claude -p "ce cauzeaza aceasta eroare?"
claude -p "genereaza un .gitignore pentru un proiect Node.js" > .gitignore
```

Print mode accepta input de pe stdin, ceea ce il face extrem de puternic. Poti trimite continutul unui fisier, output-ul unei comenzi, sau orice text — Claude il proceseaza si raspunde pe stdout. Combina asta cu `--output-format json` si ai un tool programatic complet.

**Continuation mode (`-c` si `-r`)** — reia o sesiune anterioara:

```bash
claude -c                     # Continua cea mai recenta sesiune
claude -c -p "mai adauga teste"  # Continua in print mode (non-interactiv)
claude -r SESSION_ID          # Reia o sesiune specifica dupa ID
```

Flag-ul `-c` (sau `--continue`) reia ultima sesiune din directorul curent. `-r` (sau `--resume`) accepta un ID de sesiune specific. Amandoua functioneaza atat in mod interactiv cat si in print mode — poti continua o conversatie anterioara non-interactiv, ceea ce e util in scripturi care lucreaza in mai multi pasi.

**Headless mode** — pentru automatizari complete, fara terminal:

```bash
claude -p --verbose "analizeaza codul" --output-format stream-json
```

Cu `--output-format stream-json`, Claude emite fiecare eveniment ca un obiect JSON pe o linie separata. Asta permite integrarea cu alte tool-uri care parseaza output-ul in timp real — dashboards, CI/CD pipelines, sau aplicatii custom.

### Flag-uri esentiale

Acestea sunt flag-urile pe care le vei folosi cel mai des, grupate dupa functionalitate:

**Control sesiune:**

| Flag | Ce face |
|------|---------|
| `-p, --print` | Print mode — raspunde si iese |
| `-c, --continue` | Continua ultima sesiune |
| `-r, --resume SESSION_ID` | Reia o sesiune specifica |
| `--verbose` | Afiseaza detalii despre tool calls si procesare |
| `--no-input` | Ruleaza fara a astepta input (util cu `-c -p`) |

**Model si performanta:**

| Flag | Ce face |
|------|---------|
| `--model MODEL` | Seteaza modelul: `opus`, `sonnet`, `haiku` |
| `--effort LEVEL` | Nivel de efort: `low`, `medium`, `high`, `max` |
| `--fast` | Activeaza modul rapid (acelasi model, output mai rapid) |

**Directoare si context:**

| Flag | Ce face |
|------|---------|
| `--add-dir CALE` | Adauga un director suplimentar in context |
| `--project-dir CALE` | Seteaza directorul proiectului (de unde se citeste CLAUDE.md) |

Flag-ul `--add-dir` e deosebit de util cand lucrezi cu un monorepo sau cand ai nevoie de context din mai multe directoare simultan. Poti adauga multiple directoare:

```bash
claude --add-dir ../shared-lib --add-dir ../api-types
```

**Output si format:**

| Flag | Ce face |
|------|---------|
| `--output-format FORMAT` | `text` (default), `json`, `stream-json` |
| `--max-turns N` | Limiteaza numarul de turn-uri (util in automatizari) |

Cu `--output-format json`, raspunsul vine structurat:

```bash
claude -p "cate fisiere TypeScript sunt?" --output-format json
# {"type":"result","subtype":"success","cost_usd":0.003,"result":"...","session_id":"..."}
```

**System prompt:**

| Flag | Ce face |
|------|---------|
| `--system-prompt TEXT` | Inlocuieste system prompt-ul complet |
| `--append-system-prompt TEXT` | Adauga la system prompt-ul existent |

`--system-prompt` inlocuieste tot ce ar primi Claude in mod normal (inclusiv CLAUDE.md). E puternic dar periculos — pierzi toate instructiunile de proiect. `--append-system-prompt` e mai sigur: adauga instructiuni suplimentare fara sa stearga ce exista deja.

```bash
# Adauga o regula temporara fara sa modifici CLAUDE.md
claude --append-system-prompt "Raspunde doar in limba romana"
```

**Permisiuni:**

| Flag | Ce face |
|------|---------|
| `--allowedTools TOOLS` | Lista de tool-uri permise (fara confirmare) |
| `--disallowedTools TOOLS` | Lista de tool-uri interzise |
| `--permission-mode MODE` | `default`, `plan`, `bypassPermissions` |

Flag-urile de permisiuni sunt esentiale pentru automatizari. In mod normal, Claude cere confirmare pentru operatiuni sensibile. Cu `--allowedTools`, poti pre-aproba anumite tool-uri:

```bash
claude -p "ruleaza testele si fix-uieste erorile" \
  --allowedTools "Bash(npm test)" "Bash(npm run lint)" "Edit" "Read"
```

### Comenzi de administrare

Pe langa `claude` (conversatie), CLI-ul ofera comenzi separate pentru administrare:

```bash
claude update                 # Actualizeaza la ultima versiune
claude auth login             # Autentificare
claude auth logout            # Deconectare
claude auth status            # Verifica statusul autentificarii
claude config                 # Deschide configurarea interactiva
claude config set KEY VALUE   # Seteaza o valoare direct
claude config get KEY         # Citeste o valoare
claude mcp                    # Gestioneaza serverele MCP
claude plugin                 # Gestioneaza plugin-urile
claude agents                 # Administreaza agentii
```

`claude config` merita atentie speciala. Poti configura totul din linia de comanda:

```bash
claude config set model opus
claude config set autoMemoryEnabled false
claude config set sessionRetentionDays 60
```

## Ghid practic pas cu pas

### Scenariul 1: Script de code review automat

Vrei sa rulezi un code review automat pe fiecare PR. Combini print mode cu pipe-uri:

```bash
#!/bin/bash
# review-pr.sh — ruleaza automat pe PR-uri noi

DIFF=$(gh pr diff)
COMMENTS=$(gh pr view --comments)

echo "$DIFF" | claude -p \
  --append-system-prompt "Esti un code reviewer. Analizeaza diff-ul si raporteaza: securitate, performanta, stil." \
  --output-format json \
  --max-turns 3 \
  --allowedTools "Read" "Grep" "Glob"
```

Acest script: preia diff-ul PR-ului curent, il trimite lui Claude in print mode cu instructiuni specifice de review, limiteaza la 3 turn-uri (sa nu intre intr-un loop), permite doar tool-uri read-only si returneaza JSON parsabil.

### Scenariul 2: Continuare multi-pas

Lucrezi la o refactorizare in mai multi pasi, fiecare intr-o sesiune separata dar in continuarea celei anterioare:

```bash
# Pasul 1: analiza
claude "analizeaza modulul de plati si propune o strategie de refactorizare"

# [mai tarziu, dupa ce ai revizuit propunerea]

# Pasul 2: implementare (continua aceeasi sesiune)
claude -c "implementeaza strategia propusa, incepand cu payment-gateway.ts"

# Pasul 3: teste (continua aceeasi sesiune)
claude -c "scrie teste pentru modificarile facute"
```

Fiecare `-c` reia exact de unde ai ramas — cu tot contextul, toate fisierele citite, toate deciziile luate.

### Scenariul 3: Procesare batch cu pipe-uri

Vrei sa generezi documentatie pentru mai multe fisiere:

```bash
# Genereaza JSDoc pentru toate fisierele din src/utils/
for file in src/utils/*.ts; do
  echo "Processing $file..."
  claude -p "adauga comentarii JSDoc la functiile din acest fisier" < "$file" > "${file}.documented"
  mv "${file}.documented" "$file"
done
```

Sau mai elegant, folosind bundled skill-ul `/batch` intr-o sesiune interactiva.

## Configurari de referinta

### Variabile de mediu utile

```bash
CLAUDE_MODEL=opus              # Model implicit
CLAUDE_MAX_TURNS=10            # Limita turn-uri in print mode
ANTHROPIC_API_KEY=sk-...       # API key (daca nu folosesti autentificarea integrata)
```

### Alias-uri recomandate

Adauga in `.zshrc` sau `.bashrc`:

```bash
alias cc="claude"
alias ccp="claude -p"
alias ccr="claude -c"
alias ccm="claude --model"
```

## Greseli frecvente si cum le eviti

**Greseala: Folosesti `--system-prompt` cand voiai `--append-system-prompt`.**
`--system-prompt` inlocuieste TOTUL — inclusiv CLAUDE.md, regulile de proiect si instructiunile de siguranta. Rezultatul: Claude se comporta complet diferit de ce asteptai. Solutia: foloseste aproape intotdeauna `--append-system-prompt`. Rezerva `--system-prompt` doar pentru cazuri in care vrei deliberat un comportament complet custom (ex: un script izolat care nu are legatura cu proiectul).

**Greseala: Print mode fara `--max-turns` in automatizari.**
In print mode, Claude poate decide sa faca mai multe turn-uri (citeste fisiere, ruleaza comenzi, itereaza). Intr-un script CI/CD, asta poate insemna timp si cost neprevazut. Solutia: seteaza intotdeauna `--max-turns` in automatizari. Valori tipice: 1-3 pentru intrebari simple, 5-10 pentru task-uri complexe.

**Greseala: Nu folosesti `--allowedTools` in scripturi.**
Fara tool-uri pre-aprobate, Claude cere confirmare interactiva — ceea ce blocheaza un script automatizat. Solutia: specifica explicit ce tool-uri sunt permise. Pentru task-uri read-only: `--allowedTools "Read" "Grep" "Glob"`. Pentru task-uri cu modificari: adauga `"Edit"` si `"Write"`.

**Greseala: Ignori `--output-format json` cand parsezi output-ul.**
Daca parsezi raspunsul lui Claude cu grep sau awk pe text plain, orice schimbare de formatare iti sparge scriptul. Solutia: foloseste `--output-format json` si parseaza cu `jq`. Output-ul JSON are structura stabila si predictibila.

## Exercitii practice

**Exercitiu 1 — Print mode de baza:**
Ruleaza `claude -p "ce versiune de Node.js am instalata?"` si observa cum raspunde si iese imediat. Apoi incearca cu pipe: `echo "console.log('hello')" | claude -p "ce face acest cod?"`. Compara cu modul interactiv.

**Exercitiu 2 — Continuare sesiune:**
Deschide o sesiune interactiva, pune o intrebare despre un fisier din proiect, apoi inchide (Ctrl+C). Acum ruleaza `claude -c` si verifica ca sesiunea continua exact de unde ai ramas, cu tot contextul intact.

**Exercitiu 3 — Script automatizat:**
Scrie un script Bash care primeste un path ca argument si foloseste `claude -p` cu `--output-format json` ca sa genereze un rezumat al fisierului. Parseaza raspunsul cu `jq` si afiseaza doar campul `result`.

## Recapitulare

CLI-ul Claude Code ofera patru moduri de lansare: interactiv (conversatie), print mode (one-shot pentru scripturi), continuation (reia sesiuni) si headless (stream JSON pentru automatizari). Flag-urile controleaza modelul, permisiunile, formatul output-ului si system prompt-ul. Comenzile de administrare gestioneaza update-uri, autentificare, configurare si servere MCP. Combinand print mode cu pipe-uri shell si `--output-format json`, transformi Claude Code dintr-un asistent conversational intr-un tool programatic complet, integrabil in orice workflow de dezvoltare.

Cu Batch 1 complet (comenzi slash, memorie, checkpoints, CLI), ai fundamentele necesare. In modulul urmator, treci la nivel intermediar cu skills — cum sa construiesti automatizari sofisticate care combina tot ce ai invatat pana acum.

---

[<< Modulul anterior: Checkpoints](../03-checkpoints/README.md) | [Cuprins](../README.md) | [Modulul urmator: Skills >>](../05-skills/README.md)
