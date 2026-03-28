# Checkpoints

> **Nivel:** Incepator | **Durata estimata:** 30 min | **Modul:** 03 din 10

[<< Modulul anterior: Memorie si CLAUDE.md](../02-memorie/README.md) | [Cuprins](../README.md) | [Modulul urmator: Referinta CLI >>](../04-cli/README.md)

---

## Ce vei invata

- Cum functioneaza sistemul de checkpoints si ce se salveaza automat
- Cum sa faci rewind la cod, conversatie, sau ambele — si cand sa alegi fiecare varianta
- Cum sa folosesti Summarize pentru a elibera context fara sa pierzi informatia
- Ce NU se salveaza in checkpoints si cum sa te protejezi
- Diferenta intre checkpoints si version control (Git)

## De ce conteaza

Checkpoints sunt plasa ta de siguranta. Fara ele, fiecare cerere catre Claude Code e un pariu: daca rezultatul nu e ce vrei, trebuie sa identifici manual ce s-a schimbat, sa anulezi modificarile si sa incerci din nou. Cu proiecte de zeci sau sute de fisiere, asta devine un cosmar.

Cu checkpoints, abordarea se schimba fundamental. In loc sa fii precaut si sa ceri modificari mici, incrementale ("modifica doar acest fisier, nimic altceva"), poti fi ambitions: "refactorizeaza intregul modul de autentificare sa foloseasca JWT in loc de sesiuni". Daca rezultatul nu e ce vrei, faci rewind in doua secunde si esti exact unde erai inainte — cod si conversatie, ca si cum nu s-ar fi intamplat nimic.

Asta schimba modul in care lucrezi. Nu mai gandesti defensiv ("sa nu strice ceva") ci ofensiv ("hai sa incercam si vedem"). Checkpoints transforma experimentarea din risc in rutina.

## Cum functioneaza

### Salvarea automata — nu trebuie sa faci nimic

De fiecare data cand trimiti un mesaj catre Claude Code, sistemul creeaza automat un checkpoint. Checkpoint-ul captureaza starea fisierelor tale inainte de orice modificare pe care Claude o face in acel turn. Nu trebuie sa activezi nimic, nu trebuie sa salvezi manual — se intampla in background, transparent.

Cateva detalii importante:
- **Fiecare prompt** = un checkpoint nou. Daca ai trimis 15 mesaje intr-o sesiune, ai 15 puncte la care poti reveni.
- **Checkpoints persista intre sesiuni.** Daca faci `/resume` si continui o conversatie mai veche, checkpoint-urile anterioare sunt inca acolo.
- **Curatare automata** dupa 30 de zile (configurabil). Nu se acumuleaza la infinit.

### Rewind — cum revii la o stare anterioara

Ai doua modalitati de a accesa rewind:

**Metoda rapida:** apasa `Esc` de doua ori (`Esc` + `Esc`). Se deschide un meniu scrollabil cu toate mesajele tale din sesiune — fiecare e un checkpoint.

**Metoda explicita:** scrie `/rewind` (sau aliasul `/checkpoint`).

In ambele cazuri, selectezi punctul la care vrei sa revii si apoi alegi una din cinci actiuni:

### Cele cinci actiuni disponibile

**1. Restore code and conversation**
Revine complet — atat codul cat si conversatia se resetau la starea de la acel punct. E ca si cum tot ce s-a intamplat dupa acel moment nu a existat niciodata. Aceasta e actiunea pe care o vei folosi cel mai des — cand Claude a luat-o pe un drum gresit si vrei sa incerci altceva.

**2. Restore conversation**
Revine doar conversatia la acel punct, dar pastreaza codul asa cum e acum. Util cand Claude a facut modificari bune de cod, dar conversatia a deraiat (de exemplu, ai intrat intr-o discutie lunga care a consumat context inutil). Vrei sa pastrezi codul dar sa "uiti" discutia.

**3. Restore code**
Revine codul la starea de la acel punct, dar pastreaza conversatia intacta. Util cand conversatia contine informatii valoroase (explicatii, decizii arhitecturale) pe care nu vrei sa le pierzi, dar codul generat nu e ce vrei.

**4. Summarize from here**
Nu revine la nimic — in schimb, comprima tot ce s-a intamplat de la acel punct intr-un rezumat generat de AI. Mesajele de dinainte raman intacte, cele de dupa devin un summary compact. Fisierele de pe disc nu se modifica.

Gandeste-te la asta ca un `/compact` tintit: in loc sa comprimi toata conversatia, pastrezi inceputul in detaliu si comprimi doar partea care ocupa spatiu inutil. Poti adauga instructiuni optionale pentru a ghida ce sa pastreze summary-ul.

**5. Never mind**
Inchide meniul fara sa faca nimic. Util cand ai deschis rewind-ul din greseala sau vrei doar sa te uiti la istoricul mesajelor.

Dupa ce restaurezi conversatia sau faci summarize, prompt-ul original de la mesajul selectat se restaureaza in campul de input — poti sa il retrimiti asa cum e sau sa il editezi inainte.

### Rewind vs. Fork — cand folosesti ce

Rewind si fork sunt complementare, dar servesc scopuri diferite:

**Rewind** (`Esc Esc` sau `/rewind`) revine in trecut — sterge ce s-a intamplat si te pune inapoi la un punct anterior. Foloseste cand Claude a gresit si vrei sa incerci altceva.

**Fork** (`/branch` sau `/fork`) creeaza o ramificatie — pastreaza sesiunea originala intacta si porneste o copie din acel punct. Foloseste cand vrei sa explorezi doua abordari diferite in paralel, fara sa pierzi niciuna.

**Summarize** comprima fara sa stearga — textul original ramane accesibil in transcript-ul sesiunii. Foloseste cand conversatia a devenit prea lunga si ai nevoie de context liber, dar nu vrei sa pierzi informatia.

| Vreau sa... | Foloseste |
|---|---|
| Anulez ce a facut Claude si incerc altceva | Rewind → Restore code and conversation |
| Pastrez codul dar resetez conversatia | Rewind → Restore conversation |
| Pastrez conversatia dar anulez codul | Rewind → Restore code |
| Incerc doua abordari simultan | `/fork` (pastreaza originalul) |
| Eliberez context din conversatie | Rewind → Summarize from here |
| Eliberez context din toata conversatia | `/compact` |

## Ghid practic pas cu pas

### Scenariul 1: Refactorizare care nu merge

```
Tu: refactorizeaza modulul de plati sa foloseasca Stripe in loc de PayPal
Claude: [modifica 8 fisiere, adauga dependinte, schimba API-ul]
Tu: [testezi — nu compileaza, prea multe schimbari odata]

# Rewind:
Esc + Esc → selectezi mesajul tau → Restore code and conversation

# Acum incerci o abordare incrementala:
Tu: schimba doar payment-gateway.ts sa foloseasca Stripe API. Nu modifica nimic altceva inca.
```

### Scenariul 2: Conversatie prea lunga

Ai inceput sesiunea cu o cerinta clara, apoi ai debuguit 20 de minute un import gresit. Codul e acum corect, dar ai consumat mult context pe debugging.

```
# Rewind:
Esc + Esc → selectezi mesajul unde a inceput debugging-ul → Summarize from here

# Instructiune optionala: "pastreaza doar solutia finala si ce a cauzat bug-ul"
```

Acum ai context liber pentru urmatoarele cerinte, dar informatia esentiala din debugging e pastrata in summary.

### Scenariul 3: Explorare de alternative

```
Tu: propune doua arhitecturi pentru sistemul de notificari

# Claude propune Arhitectura A
Tu: implementeaza Arhitectura A
Claude: [implementeaza]

# Vrei sa vezi si Arhitectura B fara sa pierzi A:
/fork

# In sesiunea fork-uita:
Tu: implementeaza Arhitectura B
Claude: [implementeaza]

# Acum ai ambele variante in sesiuni separate — compari si alegi
```

## Configurari de referinta

### Retentie checkpoints

Checkpoints se sterg automat dupa 30 de zile (impreuna cu sesiunile). Poti configura retentia in settings:

```json
{
  "sessionRetentionDays": 60
}
```

### Shortcut rapid

`Esc` + `Esc` = deschide rewind-ul instant. E cel mai rapid mod de a accesa checkpoint-urile — memoreaza-l, il vei folosi des.

## Greseli frecvente si cum le eviti

**Greseala: Te bazezi pe checkpoints pentru modificari facute prin Bash.**
Checkpoints salveaza doar modificarile facute prin tool-urile de editare ale lui Claude (Read, Edit, Write). Daca Claude ruleaza o comanda Bash care modifica fisiere (`rm`, `mv`, `cp`, `sed`), acele modificari NU se pot anula prin rewind. Solutia: pentru operatiuni distructive, asigura-te ca ai un commit Git inainte. Sau cere-i lui Claude sa foloseasca tool-urile de editare in loc de comenzi shell.

**Greseala: Confunzi checkpoints cu Git.**
Checkpoints sunt "local undo" — rapide si convenabile pentru sesiunea curenta. Nu inlocuiesc Git. Daca ai ajuns la o stare buna dupa cateva rewind-uri, fa un commit Git ca sa o pastrezi permanent. Checkpoints se sterg dupa 30 de zile — commit-urile Git raman pentru totdeauna.

**Greseala: Nu folosesti rewind cand ar trebui.**
Multi utilizatori incearca sa corecteze verbal ("nu, anuleaza ce ai facut si fa altceva"). Asta consuma context inutil si rezultatul e adesea inconsistent — Claude incearca sa "repare" in loc sa o ia de la zero. Rewind e mai curat: sterge complet tentativa esuata si iti da un fresh start.

**Greseala: Modifici fisiere manual in timp ce Claude lucreaza.**
Checkpoints nu salveaza modificarile tale manuale — doar pe cele facute de Claude in sesiunea curenta. Daca editezi un fisier in VS Code in timp ce Claude lucreaza pe el, rewind-ul poate produce stari inconsistente. Solutia: lasa Claude sa termine, verifica rezultatul, apoi fa rewind daca e nevoie.

## Exercitii practice

**Exercitiu 1 — Rewind de baza:**
Deschide Claude Code intr-un proiect. Cere-i sa adauge un comentariu la inceputul unui fisier. Apoi cere-i sa mai adauge un comentariu. Acum fa `Esc + Esc` si selecteaza primul mesaj → Restore code and conversation. Verifica ca al doilea comentariu a disparut. Simplu — dar acum stii exact cum functioneaza.

**Exercitiu 2 — Summarize:**
Intr-o sesiune, pune 4-5 intrebari despre un fisier din proiect (ce face, cum functioneaza, de ce e scris asa). Apoi fa `Esc + Esc`, selecteaza a doua intrebare → Summarize from here. Observa cum toate intrebarile si raspunsurile au fost comprimate intr-un singur rezumat, eliberand context.

**Exercitiu 3 — Fork pentru alternative:**
Cere-i lui Claude sa scrie o functie intr-un anumit stil. Apoi fa `/fork` si in sesiunea noua cere-i aceeasi functie intr-un stil diferit. Compara rezultatele si alege varianta preferata.

## Recapitulare

Checkpoints se creeaza automat la fiecare mesaj trimis, fara interventia ta. Cu `Esc + Esc` sau `/rewind`, poti reveni la orice punct din sesiune — cod, conversatie, sau ambele. Summarize comprima parti din conversatie fara sa modifice fisierele. Fork creeaza ramificatii pentru explorare paralela. Checkpoints nu salveaza modificari Bash si nu inlocuiesc Git — sunt "undo rapid" la nivel de sesiune, nu version control permanent.

Cu checkpoints in buzunar, ai curajul sa experimentezi liber. In modulul urmator, vei invata referinta CLI — toate modurile in care poti lansa si configura Claude Code din terminal, de la flag-uri de baza pana la automatizari cu pipe-uri si scripturi.

---

[<< Modulul anterior: Memorie si CLAUDE.md](../02-memorie/README.md) | [Cuprins](../README.md) | [Modulul urmator: Referinta CLI >>](../04-cli/README.md)
