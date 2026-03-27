Genereaza sau actualizeaza modulul $ARGUMENTS din Ghidul Claude Code in romana.

## Harta modulelor

| Nr | Director | Titlu | Nivel | Durata | Prev | Next |
|----|----------|-------|-------|--------|------|------|
| 01 | 01-comenzi-slash | Comenzi Slash | Incepator | 30 min | - | 02-memorie |
| 02 | 02-memorie | Memorie si CLAUDE.md | Incepator | 45 min | 01-comenzi-slash | 03-checkpoints |
| 03 | 03-checkpoints | Checkpoints | Incepator | 30 min | 02-memorie | 04-cli |
| 04 | 04-cli | Referinta CLI | Incepator | 30 min | 03-checkpoints | 05-skills |
| 05 | 05-skills | Skills | Intermediar | 1 ora | 04-cli | 06-hooks |
| 06 | 06-hooks | Hooks | Intermediar | 1 ora | 05-skills | 07-mcp |
| 07 | 07-mcp | MCP (Model Context Protocol) | Intermediar | 1 ora | 06-hooks | 08-sub-agenti |
| 08 | 08-sub-agenti | Sub-agenti | Intermediar | 1.5 ore | 07-mcp | 09-features-avansate |
| 09 | 09-features-avansate | Functionalitati Avansate | Avansat | 2 ore | 08-sub-agenti | 10-plugins |
| 10 | 10-plugins | Plugins | Avansat | 2 ore | 09-features-avansate | - |

## Pas 0: Identifica modulul

1. Extrage numarul modulului din $ARGUMENTS (ex: "01", "05", "07")
2. Gaseste randul corespunzator in harta de mai sus
3. Verifica daca `/Users/danielbors/Projects/AI-Projects/ghid-claude-code/[director]/README.md` exista si are continut (nu doar placeholder)
   - Daca e placeholder sau nu exista → mod CREARE
   - Daca are continut real → mod ACTUALIZARE (pastreaza si extinde, nu rescrie)

## Pas 1: Cercetare

### Sursa A: Context7
1. Apeleaza `resolve-library-id` cu "Claude Code"
2. Apeleaza `query-docs` cu ID-ul gasit, focusat pe tema specifica modulului (ex: pentru modulul 06, cauta "hooks PreToolUse PostToolUse SessionStart configuration")

### Sursa B: Web Search (obligatorie)
1. Cauta informatii actuale despre tema modulului — documentatie oficiala, articole, tutoriale
2. Prioritizeaza docs.anthropic.com si surse oficiale Anthropic

### Sursa C: GitHub claude-howto (referinta de acoperire)
1. Verifica ce acopera modulul echivalent din https://github.com/luongnv89/claude-howto
2. Foloseste ca referinta de COMPLETITUDINE — asigura-te ca acoperi cel putin aceleasi concepte
3. NU copia text — rescrie cu tonul practic-tutorial stabilit, din perspectiva cuiva care foloseste Claude Code zilnic

## Pas 2: Generare modul

### Limba
Romana. NU traduce termeni tehnici (hooks, skills, slash commands, checkpoints, plugins, MCP, sub-agents, CLI, etc.). Traduce doar explicatiile.

### Dimensiune
- **Mod CREARE:** 1500-2500 cuvinte. Fiecare concept merita profunzime.
- **Mod ACTUALIZARE:** >= dimensiunea existenta. Nu scurta, doar adauga.

### Ton
Scrie ca un expert pasionat care foloseste Claude Code zilnic si vrea sa-l faca pe cititor sa inteleaga nu doar CE, ci si DE CE conteaza fiecare functionalitate. Perspectiva din interior. Exemple concrete din utilizare reala. Compara cu lucruri familiare.

### Structura obligatorie

```markdown
# [Titlu Modul]

> **Nivel:** Incepator/Intermediar/Avansat | **Durata estimata:** X min/ore | **Modul:** NN din 10

[<< Modulul anterior: Titlu](../prev-dir/README.md) | [Cuprins](../README.md) | [Modulul urmator: Titlu >>](../next-dir/README.md)

---

## Ce vei invata

3-5 bullet points cu rezultatele concrete ale acestui modul. Nu "vei intelege conceptul X" — ci "vei sti sa configurezi X si sa il folosesti pentru Y".

## De ce conteaza

3-4 paragrafe care explica DE CE aceasta functionalitate exista, ce problema rezolva, si ce se intampla fara ea. Perspectiva practica — scenarii reale in care face diferenta. Aceasta sectiune e cea care transforma un cititor sceptic in unul convins.

## Cum functioneaza

### Concept 1 — Titlu descriptiv
4-5 randuri de explicatie. Ce este, cum se leaga de restul, o analogie daca ajuta.

Exemplu practic (cod, configurare, sau comanda):
```[limbaj]
# exemplu cu comentarii inline
```

### Concept 2 — Titlu descriptiv
...

(Continua pentru 4-7 concepte, in functie de complexitatea modulului)

## Ghid practic pas cu pas

Parcurs concret, actionabil — "fa asta, apoi asta, apoi verifica asta":
1. Pas cu comanda exacta si output asteptat
2. ...
3. ...

Include configurari complete, copy-paste ready. Cititorul trebuie sa poata urma pasii si sa obtina un rezultat functional.

## Configurari de referinta

1-3 exemple complete de configurare pentru scenarii reale (nu academice). Fiecare cu:
- Contextul: "Aceasta configurare e pentru..."
- Codul/config complet
- Ce face fiecare linie importanta

## Greseli frecvente si cum le eviti

3-4 greseli pe care le fac incepatorii cu aceasta functionalitate:
- **Greseala:** ce fac gresit
- **De ce e problema:** ce se intampla
- **Solutia:** cum faci corect

## Exercitii practice

2-3 exercitii pe care cititorul le poate face imediat:
1. **Exercitiu simplu** — verifica ca a inteles bazele
2. **Exercitiu intermediar** — aplica in proiectul propriu
3. **Provocare** (optional) — combina cu alte module

## Recapitulare

3-5 fraze care rezuma ce a invatat cititorul. Apoi o propozitie de tranzitie catre modulul urmator — de ce e relevant ce urmeaza.

---

[<< Modulul anterior: Titlu](../prev-dir/README.md) | [Cuprins](../README.md) | [Modulul urmator: Titlu >>](../next-dir/README.md)
```

### Sectiuni aditionale (adauga doar daca modulul le cere)
- **Diagrame** — foloseste Mermaid pentru fluxuri si arhitecturi (daca ajuta la intelegere)
- **Tabele de referinta** — pentru liste lungi de comenzi, optiuni, sau configurari
- **Comparatii** — cand exista mai multe abordari si cititorul trebuie sa aleaga

## Pas 3: Salvare

Salveaza modulul in:
`/Users/danielbors/Projects/AI-Projects/ghid-claude-code/[director]/README.md`

**NU publica automat in Notion** — publicarea se face separat, pentru tot ghidul odata.

## Pas 4: Confirma

Raporteaza:
- Modul generat (numar + titlu)
- Mod folosit (CREARE sau ACTUALIZARE)
- Numar de cuvinte
- Lista sectiunilor
- Concepte acoperite
- Daca ACTUALIZARE: ce s-a schimbat
