# Hooks

> **Nivel:** Intermediar | **Durata estimata:** 1 ora | **Modul:** 06 din 10

[<< Modulul anterior: Skills](../05-skills/README.md) | [Cuprins](../README.md) | [Modulul urmator: MCP >>](../07-mcp/README.md)

---

## Ce vei invata

- Ce sunt hooks si cum se integreaza in ciclul de viata al unei sesiuni Claude Code
- Toate tipurile de evenimente disponibile si cand se declanseaza fiecare
- Cum sa configurezi hooks in settings.json cu matchers, tipuri si output JSON
- Cum sa blochezi operatiuni periculoase, sa auto-aprobezi actiuni sigure si sa injectezi context
- Diferenta intre hooks command, HTTP, prompt si agent
- Cum sa combini hooks cu skills pentru automatizari complete

## De ce conteaza

Skills (Modulul 05) iti dau control asupra a ce face Claude cand ii ceri. Hooks iti dau control asupra a ce se intampla *in jurul* actiunilor lui Claude — automat, fara sa intervii.

Gandeste-te la hooks ca la middleware intr-un framework web. Asa cum un middleware Express verifica autentificarea inainte de fiecare request si logheaza raspunsul dupa, hooks verifica comenzile lui Claude inainte de executie si reactioneaza la rezultate dupa. Nu trebuie sa te uiti la fiecare actiune — hooks fac asta pentru tine.

Fara hooks, securitatea depinde de atentia ta: "am observat ca Claude voia sa ruleze `rm -rf`?". Cu hooks, regulile sunt enforce-uite automat: comanda periculoasa e blocata inainte de executie, linting-ul ruleaza automat dupa fiecare fisier scris, si fiecare operatiune e logata. E diferenta intre a avea un gardian care doarme si unul care nu doarme niciodata.

## Cum functioneaza

### Ciclul de viata al unei sesiuni

Hooks se declanseaza la puncte specifice in ciclul de viata:

```
SessionStart → UserPromptSubmit → [Agentic Loop] → SessionEnd
                                       │
                                  PreToolUse (poate bloca)
                                       │
                                  PermissionRequest (poate bloca)
                                       │
                                  PostToolUse / PostToolUseFailure
                                       │
                                  SubagentStart / SubagentStop
                                       │
                                  Stop / StopFailure
```

In plus, evenimente asincrone: `FileChanged`, `ConfigChange`, `CwdChanged`, `Notification`.

### Unde configurezi hooks

| Locatie | Scop | Se commiteaza? |
|---------|------|----------------|
| `~/.claude/settings.json` | Toate proiectele tale | Nu |
| `.claude/settings.json` | Proiectul curent (echipa) | Da |
| `.claude/settings.local.json` | Proiectul curent (personal) | Nu (gitignored) |
| Frontmatter skill/agent | Cat timp componenta e activa | Da |

### Structura configurarii

Hooks se definesc in settings.json sub cheia `hooks`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/validate-bash.sh",
            "timeout": 600
          }
        ]
      }
    ]
  }
}
```

Fiecare intrare are:
- **`matcher`** — regex care filtreaza cand se declanseaza hook-ul (ex: `Bash`, `Edit|Write`, `mcp__.*`). Omis sau `"*"` = se potriveste cu totul
- **`hooks`** — lista de handlers care se executa
- **`if`** — filtru suplimentar pe tool name + argumente, folosind sintaxa de permisiuni (ex: `"Bash(git *)"`, `"Edit(*.ts)"`)

### Tipuri de handlers

**Command** — executa o comanda shell. Input-ul vine pe stdin (JSON), controlul se face prin exit codes si stdout:

```json
{
  "type": "command",
  "command": ".claude/hooks/lint-after-write.sh",
  "timeout": 600,
  "async": false
}
```

**HTTP** — trimite JSON via POST catre un endpoint:

```json
{
  "type": "http",
  "url": "http://localhost:8080/hooks/pre-tool-use",
  "headers": { "Authorization": "Bearer $MY_TOKEN" },
  "allowedEnvVars": ["MY_TOKEN"]
}
```

**Prompt** — trimite un prompt lui Claude pentru evaluare yes/no:

```json
{
  "type": "prompt",
  "prompt": "Este aceasta operatiune sigura? Argumentele: $ARGUMENTS"
}
```

**Agent** — spawneaza un sub-agent care verifica conditii:

```json
{
  "type": "agent",
  "prompt": "Verifica daca testele trec si artefactul exista"
}
```

### Exit codes si controlul fluxului

| Exit code | Efect |
|-----------|-------|
| `0` | Succes — output-ul JSON e procesat daca exista |
| `2` | Blocare — stderr-ul e trimis lui Claude; tool call-ul e blocat |
| Alt cod | Eroare non-blocanta — stderr afisat in verbose mode |

Exit code 2 blocheaza in: `PreToolUse`, `PermissionRequest`, `UserPromptSubmit`, `Stop`, `TaskCreated`. Nu blocheaza in: `PostToolUse`, `Notification`, `SessionStart`.

### Output JSON structurat

Pentru control fin, hook-urile pot returna JSON pe stdout (exit 0):

**PreToolUse — permite, blocheaza sau modifica input-ul:**

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "Comanda read-only, aprobata automat",
    "updatedInput": { "command": "npm test --verbose" },
    "additionalContext": "Context suplimentar pentru Claude"
  }
}
```

`permissionDecision` poate fi `"allow"` (auto-aproba), `"deny"` (blocheaza), sau `"ask"` (cere confirmare userului).

**PostToolUse — blocheaza dupa executie:**

```json
{
  "decision": "block",
  "reason": "Linting a esuat. Fix-uieste erorile inainte de a continua."
}
```

**Stop — impiedica oprirea:**

```json
{
  "decision": "block",
  "reason": "Testele inca nu trec. Continua sa fix-uiesti."
}
```

### Evenimentele principale

**`SessionStart`** — la inceputul fiecarei sesiuni. Matchers: `startup`, `resume`, `clear`, `compact`. Util pentru a incarca context initial (ultimele commit-uri, issues deschise).

**`UserPromptSubmit`** — dupa ce userul trimite un prompt, inainte ca Claude sa il proceseze. Poti bloca prompt-uri periculoase sau adauga context.

**`PreToolUse`** — inainte de executia unui tool. Cel mai folosit eveniment. Matchers: numele tool-ului (`Bash`, `Edit`, `Write`, `mcp__*`). Poti bloca, aproba automat, sau modifica input-ul.

**`PostToolUse`** — dupa executia cu succes a unui tool. Util pentru linting automat, validare, sau logare.

**`PermissionRequest`** — cand dialogul de permisiuni e pe punctul de a fi afisat. Poti auto-aproba sau refuza fara interventie umana.

**`Stop`** — cand Claude termina de raspuns. Poti impiedica oprirea (ex: "testele inca nu trec, continua"). **Atentie:** verifica `stop_hook_active` ca sa eviti loop-uri infinite.

**`FileChanged`** — cand un fisier se modifica pe disc. Matcher pe basename: `.env`, `*.ts`.

**`CwdChanged`** — cand directorul de lucru se schimba. Util pentru a reactualiza environment variables.

### Variabile de mediu disponibile

In hooks de tip command, ai acces la:
- `$CLAUDE_PROJECT_DIR` — radacina proiectului
- `$CLAUDE_ENV_FILE` — (doar in SessionStart, CwdChanged, FileChanged) cale catre un fisier unde poti persista variabile de mediu
- `$CLAUDE_CODE_REMOTE` — `"true"` in medii remote/web

## Ghid practic pas cu pas

### Scenariul 1: Blocheaza comenzi periculoase

Creeaza `.claude/hooks/validate-bash.sh`:

```bash
#!/bin/bash
COMMAND=$(jq -r '.tool_input.command' < /dev/stdin)

# Blocheaza pattern-uri distructive
if echo "$COMMAND" | grep -Eq '(rm -rf|:(){|fork\(\))'; then
  jq -n '{
    "hookSpecificOutput": {
      "hookEventName": "PreToolUse",
      "permissionDecision": "deny",
      "permissionDecisionReason": "Comanda distructiva blocata automat"
    }
  }'
  exit 0
fi

exit 0
```

Fa-l executabil si configureaza in `.claude/settings.local.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/validate-bash.sh"
          }
        ]
      }
    ]
  }
}
```

### Scenariul 2: Lint automat dupa scriere

```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path')

if [[ "$FILE_PATH" == *.ts ]]; then
  LINT_OUTPUT=$(npx eslint "$FILE_PATH" 2>&1)
  if [ $? -ne 0 ]; then
    jq -n --arg reason "Linting esuat: $LINT_OUTPUT" '{
      "decision": "block",
      "reason": $reason
    }'
    exit 0
  fi
fi

exit 0
```

Configurat pe `PostToolUse` cu matcher `Write|Edit`.

### Scenariul 3: Context automat la start sesiune

```bash
#!/bin/bash
echo "Ultimele 5 commit-uri:"
git log -5 --oneline 2>/dev/null || echo "Nu e un repo git"
echo ""
echo "Branch curent: $(git branch --show-current 2>/dev/null)"
exit 0
```

Output-ul devine context pe care Claude il vede la inceputul sesiunii.

### Scenariul 4: Auto-aproba operatiuni read-only

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "Bash",
        "if": "Bash(git status)",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\":{\"hookEventName\":\"PermissionRequest\",\"decision\":{\"behavior\":\"allow\"}}}'"
          }
        ]
      }
    ]
  }
}
```

## Configurari de referinta

### Hook de audit complet

Logheaza fiecare tool call intr-un fisier:

```bash
#!/bin/bash
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')
TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "$TIME | $TOOL | $(whoami)" >> ~/.claude/tool-audit.log
exit 0
```

Pe `PostToolUse` fara matcher (se aplica pe toate tool-urile). Cu `"async": true` ca sa nu incetineasca sesiunea.

### Hooks in skills

Poti defini hooks direct in frontmatter-ul unui skill:

```yaml
---
name: secure-deploy
description: Deploy cu verificari de securitate
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
          once: true
---
```

Campul `once` face ca hook-ul sa ruleze o singura data pe sesiune. Hook-urile din skills sunt active doar cat timp skill-ul e in uz.

## Greseli frecvente si cum le eviti

**Greseala: Loop infinit in hook-ul Stop.**
Daca hook-ul de Stop blocheaza mereu oprirea, Claude intra intr-un loop infinit. Solutia: verifica intotdeauna campul `stop_hook_active` din input — daca e `true`, inseamna ca Claude deja a fost readus de un hook anterior. Lasa-l sa se opreasca.

**Greseala: Hook-uri lente pe SessionStart.**
Un hook care dureaza 10 secunde pe SessionStart incetineste fiecare pornire de sesiune. Solutia: pastreaza hook-urile de start rapide. Muta operatiuni lente in hooks async (`"async": true`) sau in PostToolUse.

**Greseala: Nu parsezi stdin cu jq.**
Hook-urile primesc JSON pe stdin. Daca il parsezi cu `grep` sau `cut`, orice schimbare de format iti sparge scriptul. Solutia: foloseste `jq` intotdeauna. `jq -r '.tool_input.command'` e robust si lizibil.

**Greseala: Hook-uri fara matcher.**
Un hook pe PreToolUse fara matcher se declanseaza pe FIECARE tool call — inclusiv Read, Glob, Grep. Asta incetineste sesiunea semnificativ. Solutia: foloseste matcher-ul ca sa filtrezi doar tool-urile relevante, si campul `if` pentru filtrare si mai granulara.

## Exercitii practice

**Exercitiu 1 — Hook de blocare:**
Creeaza un hook PreToolUse pe Bash care blocheaza orice comanda care contine `sudo`. Testeaza cerand-i lui Claude sa ruleze `sudo apt update`. Verifica ca e blocat si ca Claude primeste un mesaj explicativ.

**Exercitiu 2 — Hook de audit:**
Creeaza un hook PostToolUse (fara matcher) care logheaza numele tool-ului, timestamp-ul si directorul curent intr-un fisier `~/.claude/audit.log`. Seteaza `"async": true`. Lucreaza normal o sesiune, apoi verifica log-ul.

**Exercitiu 3 — Hook combinat cu skill:**
Creeaza un skill `/safe-refactor` care are un hook PreToolUse integrat in frontmatter. Hook-ul blocheaza orice scriere in fisiere din `src/core/` fara confirmare explicita. Testeaza cerand-i lui Claude sa refactorizeze un fisier din acel director.

## Recapitulare

Hooks sunt comenzi shell, endpoint-uri HTTP, prompt-uri sau agenti care se executa automat la evenimente specifice in ciclul de viata al lui Claude Code. Le configurezi in settings.json cu matchers pentru a filtra cand se declanseaza. PreToolUse e cel mai folosit — blocheaza operatiuni periculoase, auto-aproba actiuni sigure, sau modifica input-ul inainte de executie. PostToolUse permite linting automat si validare. Exit code 2 blocheaza, exit code 0 cu JSON ofera control granular. Hooks completeaza skills: skills sunt CE face Claude, hooks sunt regulile care guverneaza CUM face.

In modulul urmator, vei invata despre MCP — cum sa conectezi Claude Code la tool-uri externe (baze de date, API-uri, issue trackers) prin Model Context Protocol. MCP extinde ce poate face Claude dincolo de fisierele locale.

---

[<< Modulul anterior: Skills](../05-skills/README.md) | [Cuprins](../README.md) | [Modulul urmator: MCP >>](../07-mcp/README.md)
