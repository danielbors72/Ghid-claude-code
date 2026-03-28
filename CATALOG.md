# Catalog functionalitatilor Claude Code

[<< Inapoi la Cuprins](README.md)

Index complet al functionalitatilor acoperite in acest ghid.

---

## Sumar

| Categorie | Functionalitati | Modul |
|-----------|----------------|-------|
| Comenzi Slash (built-in) | `/clear`, `/compact`, `/resume`, `/branch`, `/rewind`, `/context`, `/export`, `/model`, `/fast`, `/effort`, `/cost`, `/usage`, `/diff`, `/security-review`, `/pr-comments`, `/plan`, `/init`, `/memory`, `/permissions`, `/config`, `/doctor`, `/hooks`, `/mcp`, `/add-dir`, `/btw`, `/copy`, `/rename`, `/voice`, `/vim`, `/stats` | [01](01-comenzi-slash/README.md) |
| Comenzi Slash (personalizate) | SKILL.md, frontmatter YAML, `$ARGUMENTS`, `$0`-`$N`, `` !`command` ``, `@path`, `disable-model-invocation`, `context: fork`, `allowed-tools` | [01](01-comenzi-slash/README.md) |
| Bundled Skills | `/batch`, `/simplify`, `/debug`, `/loop`, `/claude-api` | [01](01-comenzi-slash/README.md), [05](05-skills/README.md) |
| Memorie si CLAUDE.md | Ierarhie locatii (organizatie > proiect > personal), importuri cu `@`, `.claude/rules/` cu `paths` frontmatter, symlinks, auto-memory, `/memory` | [02](02-memorie/README.md) |
| Checkpoints | Salvare automata, rewind (`Esc+Esc`, `/rewind`), 5 actiuni (restore code+conversation, restore conversation, restore code, summarize, never mind), fork (`/branch`) | [03](03-checkpoints/README.md) |
| CLI Reference | Mod interactiv, print mode (`-p`), continuation (`-c`, `-r`), headless (`stream-json`), `--model`, `--effort`, `--add-dir`, `--output-format`, `--system-prompt`, `--append-system-prompt`, `--allowedTools`, `--max-turns`, `claude config`, `claude auth`, `claude mcp`, `claude plugin` | [04](04-cli/README.md) |
| Skills | SKILL.md format, toate campurile frontmatter, ierarhie de prioritate, control invocare (`disable-model-invocation`, `user-invocable`), argumente si substitutii, context dinamic, `context: fork` cu `agent`, fisiere auxiliare, `${CLAUDE_SKILL_DIR}`, `${CLAUDE_SESSION_ID}` | [05](05-skills/README.md) |
| Hooks | Evenimente: SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, PermissionRequest, Stop, SubagentStart/Stop, FileChanged, CwdChanged, ConfigChange, Notification, TaskCreated/Completed. Tipuri handler: command, HTTP, prompt, agent. Exit codes, output JSON, `permissionDecision`, matchers, `if` field | [06](06-hooks/README.md) |
| MCP Servers | Transport: HTTP, SSE, stdio. Instalare cu `claude mcp add`. Scope-uri: local, project (`.mcp.json`), user. Channels, dynamic tool updates, variabile de mediu, OAuth 2.0 | [07](07-mcp/README.md) |
| Sub-agenti | Built-in: Explore, Plan, general-purpose, Bash. Custom: `.claude/agents/`, `~/.claude/agents/`, CLI `--agents`. Frontmatter: tools, disallowedTools, model, permissionMode, maxTurns, skills, mcpServers, hooks, memory, background, effort, isolation. Foreground/background, @-mention, `--agent`, memorie persistenta | [08](08-sub-agenti/README.md) |
| Functionalitati Avansate | Plan mode (`--permission-mode plan`, Shift+Tab), extended thinking (ultrathink, adaptive reasoning, effort levels), git worktrees (`--worktree`, `.worktreeinclude`), headless mode, scheduled tasks (cloud, desktop, GitHub Actions, `/loop`), agent teams, referinte `@`, imagini | [09](09-features-avansate/README.md) |
| Plugins | `plugin.json` manifest, namespace-uri, structura plugin (skills/, agents/, hooks/, .mcp.json, .lsp.json, settings.json), `--plugin-dir`, `/reload-plugins`, marketplace, conversie standalone → plugin, restrictii securitate agenti | [10](10-plugins/README.md) |

---

## Statistici

- **Module completate:** 10/10
- **Cuvinte totale:** ~22.000
- **Nivel incepator:** Module 01-04 (~2.5 ore)
- **Nivel intermediar:** Module 05-08 (~4.5 ore)
- **Nivel avansat:** Module 09-10 (~4 ore)
