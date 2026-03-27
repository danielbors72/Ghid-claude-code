# Referinta rapida

[<< Inapoi la Cuprins](README.md)

Cheat sheet cu cele mai importante comenzi si configurari. Copy-paste ready.

---

## Instalare

```bash
# macOS / Linux (recomandat)
curl -fsSL https://claude.ai/install.sh | bash

# Homebrew
brew install --cask claude-code

# Windows (PowerShell)
irm https://claude.ai/install.ps1 | iex

# Windows Package Manager
winget install Anthropic.ClaudeCode
```

---

## Pornire si moduri de lansare

```bash
claude                      # Sesiune interactiva in directorul curent
claude "explica codul"      # Comanda directa (fara sesiune interactiva)
claude -p "intrebare"       # Print mode — raspunde si iese
claude --resume             # Continua ultima sesiune
claude --model opus         # Lanseaza cu un model specific
claude config               # Deschide configurarea
```

---

## Comenzi slash esentiale

| Comanda | Ce face | Modul |
|---------|---------|-------|
| `/help` | Afiseaza ajutor | [01](01-comenzi-slash/README.md) |
| `/init` | Creeaza CLAUDE.md pentru proiect | [01](01-comenzi-slash/README.md) |
| `/compact` | Comprima contextul (elibereaza memorie) | [01](01-comenzi-slash/README.md) |
| `/clear` | Reseteaza conversatia | [01](01-comenzi-slash/README.md) |
| `/resume` | Continua sesiunea anterioara | [01](01-comenzi-slash/README.md) |
| `/diff` | Afiseaza modificarile facute | [01](01-comenzi-slash/README.md) |
| `/review` | Code review complet | [01](01-comenzi-slash/README.md) |
| `/simplify` | Propune optimizari de cod | [01](01-comenzi-slash/README.md) |
| `/model` | Schimba modelul AI | [01](01-comenzi-slash/README.md) |
| `/cost` | Afiseaza costurile sesiunii | [01](01-comenzi-slash/README.md) |
| `/memory` | Editeaza memoria persistenta | [02](02-memorie/README.md) |
| `/plan` | Activeaza planning mode | [09](09-features-avansate/README.md) |

---

## Structura fisierelor Claude Code

```
~/.claude/                          # Configurare globala (user)
├── CLAUDE.md                       # Instructiuni globale
├── settings.json                   # Permisiuni si hooks globale
├── commands/                       # Comenzi slash globale
│   └── comanda-mea.md
└── memory/                         # Memorie persistenta
    └── MEMORY.md

proiect/                            # Configurare per proiect
├── CLAUDE.md                       # Instructiuni proiect (citit automat)
└── .claude/
    ├── settings.json               # Permisiuni proiect
    ├── settings.local.json         # Permisiuni locale (gitignored)
    ├── commands/                    # Comenzi slash proiect
    │   └── deploy.md
    └── skills/                     # Skills proiect
        └── skill-name/
            └── SKILL.md
```

**Prioritate settings:** Managed (enterprise) > User (`~/.claude/`) > Project (`.claude/`) > Local (`.claude/settings.local.json`)

---

## CLAUDE.md — template minim

```markdown
# Numele Proiectului

## Structura
- `src/` — codul sursa
- `tests/` — teste

## Conventii
- Folosim TypeScript strict
- Teste cu Jest
- Commit messages in engleza

## Reguli
- Nu modifica fisierele din `vendor/`
- Ruleaza `npm test` inainte de commit
```

---

## Hooks — configurare in settings.json

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Verificare inainte de scriere...'"
          }
        ]
      }
    ]
  }
}
```

**Evenimente disponibile:** `PreToolUse`, `PostToolUse`, `SessionStart`, `Stop`

---

## MCP — configurare server

```json
// .mcp.json (in directorul proiectului)
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_..."
      }
    }
  }
}
```

---

## Permisiuni — template settings.json

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Glob",
      "Grep",
      "Bash(npm test)",
      "Bash(npm run build)"
    ],
    "deny": [
      "Bash(rm -rf *)"
    ]
  }
}
```

---

## Linkuri rapide

| Resursa | Link |
|---------|------|
| Documentatie oficiala | [docs.anthropic.com/en/docs/claude-code](https://docs.anthropic.com/en/docs/claude-code/overview) |
| Best practices | [docs.anthropic.com/.../best-practices](https://docs.anthropic.com/en/docs/claude-code/best-practices) |
| GitHub repo | [github.com/anthropics/claude-code](https://github.com/anthropics/claude-code) |
| GitHub Discussions | [github.com/.../discussions](https://github.com/anthropics/claude-code/discussions) |
| Claude Code Action | [github.com/.../claude-code-action](https://github.com/anthropics/claude-code-action) |
