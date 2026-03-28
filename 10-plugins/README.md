# Plugins

> **Nivel:** Avansat | **Durata estimata:** 2 ore | **Modul:** 10 din 10

[<< Modulul anterior: Functionalitati Avansate](../09-features-avansate/README.md) | [Cuprins](../README.md)

---

## Ce vei invata

- Ce sunt plugins si cum se deosebesc de configurarea standalone
- Cum sa creezi un plugin de la zero cu manifest, skills, agenti si hooks
- Cum sa distribui plugins prin marketplace-uri
- Cum sa convertesti configurari existente din `.claude/` intr-un plugin
- Ce securitate si limitari se aplica pe plugins
- Cum sa testezi si sa depanezi plugins in dezvoltare

## De ce conteaza

Pana acum ai creat skills in `.claude/skills/`, agenti in `.claude/agents/`, hooks in settings.json si servere MCP in `.mcp.json`. Toate functioneaza — dar sunt legate de un singur proiect sau de masina ta. Daca vrei sa le partajezi cu echipa, trebuie sa copiezi fisiere manual. Daca vrei sa le distribui comunitatii, nu ai un mecanism standard.

Plugins rezolva asta. Un plugin impacheteaza skills, agenti, hooks, servere MCP si servere LSP intr-un pachet cu identitate proprie (nume, versiune, autor) care se instaleaza cu o singura comanda. Echipa ta instaleza plugin-ul si primeste tot — fara sa copieze fisiere, fara sa configureze manual.

Gandeste-te la plugins ca la npm packages pentru Claude Code. Skills standalone sunt ca scripturile locale — functioneaza pe masina ta. Plugins sunt ca pachetele publicate — functioneaza oriunde.

## Cum functioneaza

### Structura unui plugin

Un plugin e un director cu o structura specifica:

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Manifestul (obligatoriu)
├── skills/                   # Skills (SKILL.md in subdirectoare)
│   └── code-review/
│       └── SKILL.md
├── agents/                   # Agenti custom
│   └── reviewer.md
├── commands/                 # Comenzi slash (format legacy)
│   └── deploy.md
├── hooks/
│   └── hooks.json            # Hooks specifice plugin-ului
├── .mcp.json                 # Servere MCP bundled
├── .lsp.json                 # Servere LSP pentru code intelligence
└── settings.json             # Settings default (doar `agent` suportat)
```

**Atentie:** doar `plugin.json` merge in `.claude-plugin/`. Toate celelalte directoare sunt la radacina plugin-ului.

### Manifestul — plugin.json

Manifestul defineste identitatea plugin-ului:

```json
{
  "name": "my-plugin",
  "description": "Code review automatizat cu conventii custom",
  "version": "1.0.0",
  "author": {
    "name": "Numele Tau"
  }
}
```

| Camp | Ce face |
|------|---------|
| `name` | Identificator unic si namespace pentru skills. Skills devin `/my-plugin:skill-name` |
| `description` | Afisat in plugin manager la browse si instalare |
| `version` | Semantic versioning pentru tracking releases |
| `author` | Optional, pentru atribuire |

Campuri aditionale: `homepage`, `repository`, `license`.

### Namespace-uri — de ce exista

Skills dintr-un plugin sunt prefixate cu numele plugin-ului: `/my-plugin:hello`, nu `/hello`. Asta previne conflicte cand mai multe plugins au skills cu acelasi nume. Comenzile standalone din `.claude/skills/` pastreaza numele simplu (`/hello`).

### Plugins vs. standalone — cand alegi ce

| Criteriu | Standalone (`.claude/`) | Plugin |
|----------|------------------------|--------|
| Disponibilitate | Un proiect sau personal | Orice proiect care il instaleaza |
| Partajare | Manual (copy files) | `claude plugin install` |
| Namespace | `/skill-name` | `/plugin-name:skill-name` |
| Versioning | Nu | Semantic versioning |
| Distributie | Nu | Marketplace-uri |
| Componente multiple | Fisiere separate | Pachet unitar |

**Regula practica:** incepe cu standalone in `.claude/` pentru iteratie rapida. Cand esti gata sa partajezi, converteste in plugin.

### Componente suportate

**Skills** — fisiere SKILL.md in `skills/<skill-name>/`. Suporta acelasi frontmatter ca skills standalone (description, disable-model-invocation, allowed-tools etc.). Se invoaca cu `/plugin-name:skill-name`.

**Agenti** — fisiere Markdown in `agents/`. Suporta acelasi frontmatter ca agentii custom. **Restrictie de securitate:** plugin agents NU suporta `hooks`, `mcpServers` sau `permissionMode` in frontmatter. Aceste campuri sunt ignorate la incarcare.

**Hooks** — definite in `hooks/hooks.json`. Format identic cu hooks din settings.json. Se activeaza cand plugin-ul e enabled.

**MCP servers** — definite in `.mcp.json` la radacina plugin-ului. Se conecteaza automat cand plugin-ul e activat. Suporta `${CLAUDE_PLUGIN_ROOT}` si `${CLAUDE_PLUGIN_DATA}` ca variabile de mediu.

**LSP servers** — definite in `.lsp.json`. Ofera code intelligence (go-to-definition, find-references) pentru limbaje specifice. Userul trebuie sa aiba binary-ul language server-ului instalat.

**Settings** — `settings.json` la radacina plugin-ului. Momentan suporta doar cheia `agent` (activeaza un agent al plugin-ului ca agent principal).

## Ghid practic pas cu pas

### Creeaza un plugin de la zero

**Pasul 1:** Creeaza structura:

```bash
mkdir -p my-review-plugin/.claude-plugin
mkdir -p my-review-plugin/skills/review-code
mkdir -p my-review-plugin/agents
```

**Pasul 2:** Scrie manifestul:

```json
// my-review-plugin/.claude-plugin/plugin.json
{
  "name": "review-suite",
  "description": "Code review automatizat cu verificari de securitate si calitate",
  "version": "1.0.0",
  "author": { "name": "Echipa ta" }
}
```

**Pasul 3:** Adauga un skill:

```yaml
# my-review-plugin/skills/review-code/SKILL.md
---
name: review-code
description: Analizeaza codul pentru calitate, securitate si best practices
allowed-tools: Read, Grep, Glob
---

Analizeaza fisierele modificate:
1. Calitate cod: DRY, SOLID, error handling
2. Securitate: input validation, SQL injection, XSS
3. Performanta: N+1 queries, memory leaks
4. Teste: coverage adecvat

Raporteaza pe prioritati: Critic > Avertisment > Sugestie.
Include fisier, linie si fix sugerat.
```

**Pasul 4:** Adauga un agent:

```markdown
# my-review-plugin/agents/security-reviewer.md
---
name: security-reviewer
description: Specialist securitate. Foloseste proactiv cand se modifica cod legat de autentificare, autorizare sau date sensibile.
tools: Read, Grep, Glob, Bash
model: sonnet
---

Esti un expert in securitate aplicatii. Concentreaza-te pe:
- OWASP Top 10
- Input validation si sanitization
- Autentificare si autorizare
- Gestiunea secretelor si credentialelor
- Dependency vulnerabilities
```

**Pasul 5:** Testeaza local:

```bash
claude --plugin-dir ./my-review-plugin
```

Apoi in Claude Code:

```
/review-suite:review-code
```

Foloseste `/reload-plugins` ca sa incarci modificarile fara restart.

### Adauga hooks la plugin

Creeaza `my-review-plugin/hooks/hooks.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx eslint --fix 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

### Adauga un server MCP

Creeaza `my-review-plugin/.mcp.json`:

```json
{
  "mcpServers": {
    "github-tools": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/github-helper",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

`${CLAUDE_PLUGIN_ROOT}` se rezolva la directorul plugin-ului. `${CLAUDE_PLUGIN_DATA}` e un director persistent pentru date ale plugin-ului.

### Converteste configurari existente in plugin

Daca ai deja skills si hooks in `.claude/`:

```bash
# 1. Creeaza structura plugin
mkdir -p my-plugin/.claude-plugin

# 2. Scrie manifestul
echo '{"name":"my-plugin","description":"Migrated","version":"1.0.0"}' \
  > my-plugin/.claude-plugin/plugin.json

# 3. Copiaza componentele
cp -r .claude/skills my-plugin/
cp -r .claude/agents my-plugin/
cp -r .claude/commands my-plugin/

# 4. Migreaza hooks din settings.json in hooks/hooks.json
mkdir my-plugin/hooks
# Copiaza obiectul "hooks" din settings.json in hooks/hooks.json

# 5. Testeaza
claude --plugin-dir ./my-plugin
```

### Distribuie prin marketplace

1. Adauga `README.md` cu instructiuni de instalare si utilizare
2. Versioneaza cu semantic versioning in `plugin.json`
3. Creeaza un marketplace (repo Git cu structura specifica) sau submite la marketplace-ul oficial Anthropic
4. Altii instaleaza cu `claude plugin install`

Submisie marketplace oficial:
- [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)
- [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)

## Configurari de referinta

### Plugin minimal

```
minimal-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── hello/
        └── SKILL.md
```

### Plugin complet

```
full-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── review/
│   │   └── SKILL.md
│   └── deploy/
│       └── SKILL.md
├── agents/
│   ├── reviewer.md
│   └── deployer.md
├── hooks/
│   └── hooks.json
├── .mcp.json
├── .lsp.json
├── settings.json
└── README.md
```

### Testare cu mai multe plugins simultan

```bash
claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two
```

Cand un `--plugin-dir` plugin are acelasi nume ca un plugin instalat din marketplace, copia locala are prioritate pentru acea sesiune.

## Greseli frecvente si cum le eviti

**Greseala: Pui componentele in `.claude-plugin/` in loc de radacina plugin-ului.**
Doar `plugin.json` merge in `.claude-plugin/`. `skills/`, `agents/`, `hooks/`, `.mcp.json` sunt toate la radacina plugin-ului. Solutia: verifica structura directorului inainte de testare.

**Greseala: Astepti ca plugin agents sa aiba hooks sau permissionMode.**
Din motive de securitate, agentii din plugins NU suporta `hooks`, `mcpServers` sau `permissionMode` in frontmatter. Solutia: daca ai nevoie de aceste campuri, copiaza agentul in `.claude/agents/` sau `~/.claude/agents/`.

**Greseala: Uiti namespace-ul la invocare.**
Skills din plugins se invoaca cu `/plugin-name:skill-name`, nu `/skill-name`. Solutia: obisnuieste-te cu namespace-ul. `/help` afiseaza toate skills cu namespace-ul corect.

**Greseala: Token-uri hardcodate in `.mcp.json` al plugin-ului.**
Plugin-ul se distribuie — oricine il instaleaza vede token-urile. Solutia: foloseste variabile de mediu (`${GITHUB_TOKEN}`) si documenteaza in README ce variabile trebuie setate.

## Exercitii practice

**Exercitiu 1 — Plugin minimal:**
Creeaza un plugin cu un singur skill care saluta userul. Testeaza-l cu `--plugin-dir`. Verifica ca apare in `/help` cu namespace-ul corect.

**Exercitiu 2 — Plugin cu agent si hook:**
Extinde plugin-ul cu un agent read-only de code review si un hook PostToolUse care logheaza fiecare scriere de fisier. Testeaza ca agentul apare in `/agents` si ca hook-ul se declanseaza.

**Exercitiu 3 — Migreaza un workflow:**
Ia o configurare existenta (skills + hooks) din `.claude/` si converteste-o in plugin. Testeaza ca totul functioneaza la fel dupa migrare. Compara experienta de utilizare (namespace vs. nume direct).

## Recapitulare

Plugins impacheteaza skills, agenti, hooks, servere MCP si LSP intr-un pachet distribuibil cu identitate proprie. Structura cere un manifest in `.claude-plugin/plugin.json` si componente la radacina. Skills sunt namespace-uite cu numele plugin-ului. Agentii din plugins au restrictii de securitate (fara hooks, MCP sau permissionMode in frontmatter). Testarea se face cu `--plugin-dir`, distributia prin marketplace-uri. Convertirea din standalone e directa: copiezi componentele si adaugi manifestul.

Felicitari — ai parcurs toate cele 10 module ale ghidului! Ai invatat de la comenzi slash de baza pana la plugins distribuibile. Claude Code e acum un tool pe care il cunosti in profunzime si pe care il poti personaliza si extinde pentru orice workflow de dezvoltare.

---

[<< Modulul anterior: Functionalitati Avansate](../09-features-avansate/README.md) | [Cuprins](../README.md)
