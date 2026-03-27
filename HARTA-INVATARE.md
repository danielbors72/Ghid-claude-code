# Harta de invatare

[<< Inapoi la Cuprins](README.md)

---

## Cum sa folosesti aceasta harta

Aceasta harta iti arata drumul complet de la incepator la avansat. Fiecare nivel are:
- **Module obligatorii** — parcurge-le in ordine
- **Milestone** — ce ar trebui sa stii sa faci dupa ce termini nivelul
- **Criterii de succes** — cum verifici ca ai inteles

Daca ai deja experienta, foloseste [auto-evaluarea din README](README.md#auto-evaluare--de-unde-incepi) ca sa sari la nivelul potrivit.

---

## Nivel 1: Incepator (~2.5 ore)

**Obiectiv:** Sa poti folosi Claude Code eficient in orice proiect, cu configurare de baza si plasa de siguranta.

### Parcurs

| Ordine | Modul | Durata | Ce inveti |
|--------|-------|--------|-----------|
| 1 | [01 — Comenzi Slash](01-comenzi-slash/README.md) | 30 min | Comenzile `/` built-in, categoriile lor, cum creezi comenzi personalizate |
| 2 | [02 — Memorie si CLAUDE.md](02-memorie/README.md) | 45 min | Ierarhia de memorie, cum configurezi CLAUDE.md, instructiuni persistente |
| 3 | [03 — Checkpoints](03-checkpoints/README.md) | 30 min | Cum salvezi starea sesiunii, cum faci rewind, cand folosesti fork |
| 4 | [04 — Referinta CLI](04-cli/README.md) | 30 min | Toate comenzile din terminal, flag-uri utile, moduri de lansare |

### Milestone
Dupa acest nivel, ar trebui sa poti:
- [x] Porni o sesiune Claude Code si comunica eficient in limbaj natural
- [x] Configura un `CLAUDE.md` cu regulile proiectului tau
- [x] Folosi comenzi slash built-in pentru control sesiune si code review
- [x] Crea cel putin o comanda slash personalizata simpla
- [x] Folosi checkpoints ca plasa de siguranta cand experimentezi
- [x] Lansa Claude Code cu flag-uri utile din terminal

### Criteriu de succes
Creeaza un `CLAUDE.md` pentru un proiect existent, configureaza o comanda slash personalizata si testeaz-o cu checkpoint + rewind.

---

## Nivel 2: Intermediar (~4.5 ore)

**Obiectiv:** Sa poti automatiza workflow-uri, conecta Claude la servicii externe si folosi sub-agenti pentru taskuri complexe.

**Prerequisite:** Nivel 1 completat (sau cunostinte echivalente)

### Parcurs

| Ordine | Modul | Durata | Ce inveti |
|--------|-------|--------|-----------|
| 5 | [05 — Skills](05-skills/README.md) | 1 ora | Capabilitati reutilizabile, SKILL.md, invocari automate si manuale |
| 6 | [06 — Hooks](06-hooks/README.md) | 1 ora | Evenimente, matchers, hooks de securitate si workflow |
| 7 | [07 — MCP](07-mcp/README.md) | 1 ora | Servere MCP, configurare, integrari cu Notion/GitHub/Slack |
| 8 | [08 — Sub-agenti](08-sub-agenti/README.md) | 1.5 ore | Tipuri de agenti, paralelism, context izolat, orchestrare |

### Milestone
Dupa acest nivel, ar trebui sa poti:
- [x] Crea un skill complet cu SKILL.md si resurse
- [x] Configura hooks pentru PreToolUse, PostToolUse si SessionStart
- [x] Conecta Claude Code la cel putin un serviciu extern prin MCP
- [x] Folosi sub-agenti pentru a paraleliza taskuri complexe
- [x] Combina skills + hooks intr-un workflow automat

### Criteriu de succes
Construieste un skill care foloseste un MCP server si e protejat de un hook de validare. Testeaza cu sub-agenti in paralel.

---

## Nivel 3: Avansat (~4 ore)

**Obiectiv:** Sa stapanesti functionalitati avansate si sa poti crea si distribui plugins complete.

**Prerequisite:** Nivel 2 completat

### Parcurs

| Ordine | Modul | Durata | Ce inveti |
|--------|-------|--------|-----------|
| 9 | [09 — Functionalitati Avansate](09-features-avansate/README.md) | 2 ore | Planning mode, extended thinking, background tasks, remote agents |
| 10 | [10 — Plugins](10-plugins/README.md) | 2 ore | Structura plugin, manifest.json, distributie, marketplace |

### Milestone
Dupa acest nivel, ar trebui sa poti:
- [x] Folosi planning mode pentru a proiecta implementari complexe
- [x] Configura si folosi remote agents si background tasks
- [x] Crea un plugin complet cu skills, hooks si MCP servers
- [x] Publica un plugin pe care altii il pot instala

### Criteriu de succes
Creeaza un plugin functional care combina cel putin un skill, un hook si un MCP server. Instaleaza-l intr-un proiect nou si verifica ca totul functioneaza.

---

## Dupa ce termini

Ai parcurs tot ghidul? Iata ce poti face in continuare:

1. **Contribuie la acest ghid** — deschide un PR cu imbunatatiri, exemple noi sau corectii
2. **Creeaza si distribuie plugins** — impachetea-ti workflow-urile cele mai utile si ofera-le comunitatii
3. **Exploreaza claude-howto** — [varianta in engleza](https://github.com/luongnv89/claude-howto) acopera si subiecte avansate suplimentare
4. **Urmareste noutatile** — Claude Code se actualizeaza frecvent; documentatia oficiala: [docs.anthropic.com/en/docs/claude-code](https://docs.anthropic.com/en/docs/claude-code/overview)
