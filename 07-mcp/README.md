# MCP (Model Context Protocol)

> **Nivel:** Intermediar | **Durata estimata:** 1 ora | **Modul:** 07 din 10

[<< Modulul anterior: Hooks](../06-hooks/README.md) | [Cuprins](../README.md) | [Modulul urmator: Sub-agenti >>](../08-sub-agenti/README.md)

---

## Ce vei invata

- Ce este MCP si ce problema rezolva in ecosistemul AI
- Cele trei tipuri de transport (HTTP, SSE, stdio) si cand sa le folosesti
- Cum sa instalezi, configurezi si gestionezi servere MCP din linia de comanda
- Cum sa organizezi configurarea pe scope-uri (local, proiect, user)
- Cum functioneaza channels pentru push messages si evenimente externe
- Cum sa securizezi si sa depanezi conexiunile MCP

## De ce conteaza

Pana acum, Claude Code a lucrat cu ce gaseste local: fisierele tale, terminalul, git. MCP sparge aceasta limitare. Prin Model Context Protocol, Claude Code se conecteaza la tool-uri externe — baze de date, issue trackers, API-uri, servicii cloud — si le foloseste la fel de natural ca pe Read sau Bash.

Imagineaza-ti: "implementeaza feature-ul descris in JIRA ENG-4521, verifica datele in PostgreSQL, si creeaza un PR pe GitHub". Fara MCP, ai copia manual informatiile intre sisteme. Cu MCP, Claude face totul intr-un singur flow — citeste issue-ul, interogheaza baza de date, scrie codul si deschide PR-ul.

MCP e un standard deschis ([modelcontextprotocol.io](https://modelcontextprotocol.io)), ceea ce inseamna ca exista sute de servere disponibile, de la Notion si Gmail la Postgres si Sentry. Iar daca ai nevoie de ceva custom, poti construi propriul server cu MCP SDK.

## Cum functioneaza

### Ce este un server MCP

Un server MCP este un proces (local sau remote) care expune capabilities catre Claude Code prin protocolul MCP. Fiecare server ofera:

- **Tools** — actiuni pe care Claude le poate executa (ex: `create_issue`, `query_database`, `send_email`)
- **Resources** — date pe care Claude le poate citi (ex: continutul unui document, schema unei baze de date)
- **Prompts** — template-uri predefinite pe care serverul le ofera

Claude Code descopera automat ce ofera fiecare server conectat si le face disponibile ca tool-uri in conversatie.

### Cele trei tipuri de transport

**HTTP (recomandat)** — pentru servere remote. Cel mai larg suportat transport pentru servicii cloud:

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

**SSE (Server-Sent Events)** — transport depreciat, inlocuit de HTTP. Inca functional dar nu recomandat pentru configurari noi:

```bash
claude mcp add --transport sse asana https://mcp.asana.com/sse
```

**stdio** — pentru servere locale care ruleaza ca procese pe masina ta. Ideal pentru tool-uri care au nevoie de acces direct la sistem:

```bash
claude mcp add --transport stdio --env AIRTABLE_API_KEY=your_key airtable \
  -- npx -y airtable-mcp-server
```

**Regula de alegere:** daca serverul e un serviciu cloud (Notion, GitHub, Gmail) → HTTP. Daca e un tool local sau un script custom → stdio.

### Instalarea si gestionarea serverelor

Instalarea se face cu `claude mcp add`, iar toate optiunile (`--transport`, `--env`, `--scope`, `--header`) vin **inainte** de numele serverului. Separator `--` intre numele serverului si comanda de lansare (pentru stdio):

```bash
# Server HTTP cu autentificare
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"

# Server stdio cu variabile de mediu
claude mcp add --transport stdio --env GITHUB_TOKEN=ghp_xxx github \
  -- npx -y @modelcontextprotocol/server-github

# Gestionare
claude mcp list                    # Lista serverele configurate
claude mcp get github              # Detalii despre un server
claude mcp remove github           # Sterge un server
```

Din sesiunea Claude Code, `/mcp` afiseaza statusul tuturor serverelor conectate si permite autentificarea OAuth 2.0 pentru serverele care o necesita.

### Scope-uri de configurare

Unde se salveaza configurarea determina cine o vede:

| Scope | Flag | Ce inseamna |
|-------|------|-------------|
| `local` (default) | `--scope local` | Doar tu, doar in acest proiect. Salvat in `.claude/` (gitignored) |
| `project` | `--scope project` | Toata echipa. Salvat in `.mcp.json` la radacina proiectului (se commiteaza) |
| `user` | `--scope user` | Doar tu, in toate proiectele. Salvat in `~/.claude/` |

```bash
# Server partajat cu echipa (se commiteaza in git)
claude mcp add --scope project --transport http notion https://mcp.notion.com/mcp

# Server personal (toate proiectele)
claude mcp add --scope user --transport stdio notes \
  -- npx -y @modelcontextprotocol/server-notes
```

### Fisierul `.mcp.json`

Pentru configurarea proiectului (scope `project`), se creeaza `.mcp.json` in radacina repo-ului:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_..."
      }
    },
    "database": {
      "type": "http",
      "url": "http://localhost:5000/mcp",
      "headers": {
        "Authorization": "Bearer ${DB_TOKEN}"
      }
    }
  }
}
```

**Atentie la secrete:** nu pune token-uri reale in `.mcp.json` daca il committezi. Foloseste variabile de mediu (`${DB_TOKEN}`) si seteaza-le in `.env` (gitignored) sau in configurarea locala.

### Channels — push messages de la servere

Un server MCP poate trimite mesaje direct in sesiune, permitand lui Claude sa reactioneze la evenimente externe: rezultate CI, alerte de monitoring, mesaje chat. Serverul declara capability-ul `claude/channel`, iar tu il activezi cu flag-ul `--channels` la startup.

Cazuri de utilizare: Claude reactioneaza la mesaje Telegram, notificari Discord, sau webhook-uri — fara sa verifici tu manual.

### Dynamic tool updates

Claude Code suporta notificari `list_changed` de la servere MCP. Cand un server isi actualizeaza tool-urile, prompt-urile sau resursele, Claude Code le reincarca automat fara restart. Asta permite serverelor sa se adapteze la context (ex: un server de baza de date care isi actualizeaza schema).

## Ghid practic pas cu pas

### Conecteaza-te la GitHub

```bash
# Instaleaza serverul GitHub
claude mcp add --transport stdio --env GITHUB_TOKEN=ghp_your_token github \
  -- npx -y @modelcontextprotocol/server-github

# Verifica conexiunea
claude mcp list
```

Acum in Claude Code:

```
Tu: creeaza un issue pe repo-ul meu cu titlul "Refactorizare modul auth"
Claude: [foloseste mcp__github__create_issue pentru a crea issue-ul]
```

### Conecteaza-te la Notion

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

La prima utilizare, `/mcp` va deschide fluxul OAuth 2.0 pentru autentificare.

### Construieste o configurare de echipa

1. Creeaza `.mcp.json` in radacina proiectului:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

2. Adauga in `.env` (gitignored):

```bash
GITHUB_TOKEN=ghp_your_personal_token
```

3. Commiteaza `.mcp.json`, nu `.env`. Fiecare membru al echipei isi seteaza propriul token.

### Combina MCP cu skills si hooks

Un skill care foloseste tool-uri MCP:

```yaml
---
name: triage-issues
description: Triaza issue-urile noi si le asigneaza
disable-model-invocation: true
allowed-tools: mcp__github__*, Bash(gh *)
---

Citeste ultimele 10 issue-uri noi si pentru fiecare:
1. Analizeaza titlul si descrierea
2. Asigneaza labelul potrivit (bug, feature, docs)
3. Daca e bug critic, asigneaza-l primului developer disponibil
```

Un hook care auditeaza apeluri MCP:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "mcp__.*",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/log-mcp.sh",
            "async": true
          }
        ]
      }
    ]
  }
}
```

## Configurari de referinta

### Timeout si limita de output

```bash
# Timeout la startup (default: 5 secunde)
MCP_TIMEOUT=10000 claude

# Limita de output per tool call (default: 10.000 tokeni)
MAX_MCP_OUTPUT_TOKENS=50000 claude
```

### Servere populare

| Server | Ce face | Transport |
|--------|---------|-----------|
| GitHub | Issues, PRs, repos | stdio (`npx @modelcontextprotocol/server-github`) |
| Notion | Pagini, baze de date | HTTP (`https://mcp.notion.com/mcp`) |
| PostgreSQL | Query-uri SQL | stdio (`npx @modelcontextprotocol/server-postgres`) |
| Slack | Mesaje, canale | HTTP |
| Sentry | Erori, monitoring | HTTP |
| Gmail | Email-uri, drafturi | HTTP |
| Google Calendar | Evenimente, disponibilitate | HTTP |
| Figma | Design-uri, componente | HTTP |

Lista completa: [github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

## Greseli frecvente si cum le eviti

**Greseala: Token-uri hardcodate in `.mcp.json` committuit.**
`.mcp.json` e in git — oricine vede repo-ul vede token-urile. Solutia: foloseste `${VARIABLE_NAME}` in `.mcp.json` si seteaza valorile reale in `.env` (gitignored) sau in variabile de mediu ale sistemului.

**Greseala: Prea multe servere MCP conectate simultan.**
Fiecare server adauga tool-uri in contextul lui Claude. 10 servere cu 10 tool-uri fiecare = 100 de tool-uri in context, ceea ce consuma spatiu si face Claude mai lent in a alege tool-ul potrivit. Solutia: conecteaza doar serverele de care ai nevoie activ. Foloseste scope-ul `local` pentru servere temporare.

**Greseala: Nu verifici statusul serverelor.**
Un server MCP poate fi down sau deconectat fara sa observi — Claude va esua silentios cand incearca sa il foloseasca. Solutia: ruleaza `/mcp` periodic ca sa verifici statusul. Serverele desconectate apar marcat clar.

**Greseala: Ignori avertismentele de securitate pe servere third-party.**
Serverele MCP third-party pot primi date din surse nevalidate (prompt injection). Solutia: instaleaza doar servere in care ai incredere. Foloseste hooks PreToolUse cu matcher `mcp__*` pentru a audita sau bloca anumite operatiuni MCP.

## Exercitii practice

**Exercitiu 1 — Primul server MCP:**
Instaleaza un server MCP (GitHub e cel mai accesibil daca ai un token). Verifica cu `claude mcp list` si `/mcp` in sesiune. Cere-i lui Claude sa listeze repo-urile tale sau sa citeasca un issue.

**Exercitiu 2 — Configurare de echipa:**
Creeaza un `.mcp.json` cu un server configurat cu variabile de mediu. Seteaza valorile in `.env`. Verifica ca `.env` e in `.gitignore`. Testeaza ca serverul se conecteaza corect.

**Exercitiu 3 — Skill + MCP:**
Creeaza un skill `/daily-standup` care foloseste tool-uri MCP pentru a genera un rezumat: issues asignate tie (GitHub), evenimente de azi (Calendar), si mesaje nementionate (Slack). Testeaza cu cat de multe servere ai conectate.

## Recapitulare

MCP conecteaza Claude Code la tool-uri externe prin trei tipuri de transport: HTTP (pentru servicii cloud), SSE (depreciat), si stdio (pentru procese locale). Instalezi servere cu `claude mcp add` si le gestionezi cu `list`, `get`, `remove`. Configurarea se organizeaza pe scope-uri: local (doar tu), project (echipa, via `.mcp.json`), user (tu, global). Channels permit push messages de la servere. Securizeaza token-urile cu variabile de mediu, nu hardcodate. MCP se combina natural cu skills si hooks — skills invoca tool-uri MCP, hooks auditeaza apelurile.

In modulul urmator, vei invata despre sub-agenti — cum sa delegi task-uri catre agenti specializati care lucreaza in paralel, fiecare cu propriile tool-uri si permisiuni. Sub-agentii sunt motorul din spatele bundled skills ca `/batch` si `/simplify`.

---

[<< Modulul anterior: Hooks](../06-hooks/README.md) | [Cuprins](../README.md) | [Modulul urmator: Sub-agenti >>](../08-sub-agenti/README.md)
