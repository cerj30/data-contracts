# 📘 Návod pro práci s repozitářem `data-contracts`

Tento dokument je určen všem členům týmů, kteří budou přispívat do repozitáře s Data Contracty. Přečti si ho celý před tím, než začneš pracovat.

---

## 📋 Obsah

1. [Co je GitHub a jak funguje?](#1-co-je-github-a-jak-funguje)
2. [Základní pojmy](#2-základní-pojmy)
3. [Jak se přihlásit a dostat přístup](#3-jak-se-přihlásit-a-dostat-přístup)
4. [Jak nahrát nebo upravit Data Contract](#4-jak-nahrát-nebo-upravit-data-contract)
5. [Jak vytvořit Pull Request](#5-jak-vytvořit-pull-request)
6. [Jak schválit Pull Request](#6-jak-schválit-pull-request)
7. [Pravidla repozitáře](#7-pravidla-repozitáře)
8. [Jak vytvořit Data Contract pomocí AI (doporučený postup)](#8-jak-vytvořit-data-contract-pomocí-ai-doporučený-postup)
9. [Ukázka Data Contractu v YAML](#9-ukázka-data-contractu-v-yaml)
10. [Časté chyby a jak je opravit](#10-časté-chyby-a-jak-je-opravit)

---

## 1. Co je GitHub a jak funguje?

GitHub je platforma pro sdílení a správu souborů (v našem případě Data Contractů). Funguje jako sdílená složka, ale s jedním velkým rozdílem — **každá změna je zaznamenána, kdo ji udělal a kdy**. Nikdy nemůžeš omylem smazat práci někoho jiného, protože vše je verzované.

Náš repozitář se jmenuje **`data-contracts`** a je uložen v GitHub Organization **`bank-data-contracts`**.

---

## 2. Základní pojmy

| Pojem | Vysvětlení |
|---|---|
| **Repozitář (repo)** | Složka se všemi soubory projektu |
| **Branch (větev)** | Kopie repozitáře, kde pracuješ izolovaně |
| **Commit** | Uložení změn s popisem co jsi změnil |
| **Pull Request (PR)** | Žádost o přidání tvých změn do hlavní větve |
| **Merge** | Sloučení tvých změn do hlavní větve `main` |
| **main** | Hlavní, oficiální větev — vždy stabilní |
| **CODEOWNERS** | Soubor, který určuje kdo schvaluje změny v jaké složce |

---

## 3. Jak se přihlásit a dostat přístup

### Krok 1 — Vytvoř si GitHub účet
1. Jdi na [github.com](https://github.com)
2. Klikni na **"Sign up"**
3. Vyplň email, heslo a uživatelské jméno
4. Potvrď email

### Krok 2 — Pošli své GitHub username správci
- Pošli své GitHub **username** (ne email) správci repozitáře (JalovecM)
- Správce tě přidá do Organization a do tvého týmu
- Dostaneš emailovou pozvánku — **musíš ji přijmout!**

### Krok 3 — Přijmi pozvánku
1. Zkontroluj email
2. Klikni na odkaz v pozvánce
3. Klikni **"Accept invitation"**

---

## 4. Jak nahrát nebo upravit Data Contract

> ⚠️ **NIKDY nepracuj přímo v `main` větvi!** Vždy si vytvoř vlastní branch.

### Krok 1 — Otevři repozitář
Jdi na: `https://github.com/bank-data-contracts/data-contracts`

### Krok 2 — Vytvoř novou branch
1. Klikni na tlačítko **`main`** vlevo nahoře (šedé tlačítko s ikonou větve)
2. Do textového pole napiš název své větve, například:
   ```
   feature/team6-strategy-datacontract
   ```
   > Konvence pojmenování: `feature/<nazev-tymu>-<co-delas>`
3. Klikni na **"Create branch: feature/..."**

### Krok 3 — Přejdi do složky svého týmu
Klikni na složku svého týmu, například `team6-strategy`

### Krok 4a — Nahraj nový soubor
Pokud nahráváš nový Data Contract:
1. Klikni na **"Add file"** → **"Upload files"**
2. Přetáhni soubor `datacontract.yml` do okna
3. Zkontroluj, že jsi ve správné branch (ne v `main`!)
4. Do pole **"Commit changes"** napiš popis, například:
   ```
   Add strategy datacontract v1.0
   ```
5. Klikni **"Commit changes"**

### Krok 4b — Uprav existující soubor
Pokud upravuješ existující Data Contract:
1. Klikni na soubor `datacontract.yml`
2. Klikni na **ikonu tužky** (Edit) vpravo nahoře
3. Proveď změny
4. Dole vyplň popis změny, například:
   ```
   Update schema fields in strategy datacontract
   ```
5. Zkontroluj, že je vybrána možnost **"Commit directly to `feature/...`"** (tvoje branch, ne main!)
6. Klikni **"Commit changes"**

---

## 5. Jak vytvořit Pull Request

Po commitu je potřeba požádat o začlenění změn do `main`. To se dělá přes **Pull Request**.

### Krok 1
Po commitu GitHub automaticky zobrazí žlutý banner:
> *"Your branch had recent pushes — Compare & pull request"*

Klikni na zelené tlačítko **"Compare & pull request"**

### Krok 2 — Vyplň Pull Request
- **Title:** Stručný název, např. `Add strategy datacontract v1.0`
- **Description:** Popiš co jsi přidal/změnil, např.:
  ```
  Přidán první datacontract pro Tým 6 - Strategie.
  Obsahuje schema pro tabulku dp_strategy_kpi.
  Verze: 1.0.0
  ```

### Krok 3
Klikni na zelené tlačítko **"Create pull request"**

### Krok 4 — Počkej na schválení
- GitHub automaticky přiřadí reviewera z tvého týmu (díky CODEOWNERS)
- Reviewer dostane emailové upozornění
- Po schválení klikni **"Merge pull request"** → **"Confirm merge"**

---

## 6. Jak schválit Pull Request

Pokud jsi byl označen jako reviewer:

1. Jdi do záložky **"Pull requests"** v repozitáři
2. Klikni na Pull Request který máš schválit
3. Klikni na záložku **"Files changed"** — prohlédni si co bylo změněno
4. Klikni na zelené tlačítko **"Review changes"**
5. Vyber jednu z možností:
   - ✅ **"Approve"** — změny jsou v pořádku, schvaluji
   - 💬 **"Comment"** — mám komentář, ale neschvaluji ani nezamítám
   - ❌ **"Request changes"** — jsou potřeba opravy
6. Klikni **"Submit review"**

---

## 7. Pravidla repozitáře

| Pravidlo | Popis |
|---|---|
| ✅ Pracuj vždy ve vlastní branch | Nikdy ne přímo v `main` |
| ✅ Každý tým spravuje svou složku | Neupravuj soubory v složkách jiných týmů |
| ✅ Pojmenuj branch správně | `feature/<tym>-<popis>` |
| ✅ Piš smysluplné commit zprávy | Ne jen "update" nebo "fix" |
| ✅ Každý PR musí být schválen | Minimálně 1 schválení je povinné |
| ❌ Nikdy nepush přímo do `main` | Bude zablokováno systémem |
| ❌ Neupravuj CODEOWNERS ani .github | Pouze správce repozitáře |

---

## 8. Jak vytvořit Data Contract pomocí AI (doporučený postup)

Toto je **nejjednodušší způsob**, jak vytvořit Data Contract. Místo ručního vyplňování šablony použiješ AI asistenta (Claude nebo jiný).

### Přehled workflow

```
Tvůj popis datového produktu (česky nebo anglicky)
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 1 — AI vygeneruje celý YAML soubor                    │
│  Použij: _template/prompt_contract_generator.md             │
│  Výsledek: hotový .yml soubor připravený ke commitu         │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 2 — Zkontroluj a nahraj soubor do svého team folderu  │
│  Pojmenuj soubor podle Generated Name v kebab-case:         │
│  např. customer-service-interaction-performance.yml         │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 3 — Vytvoř Pull Request                               │
│  CI validátor automaticky zkontroluje soubor                │
│  Po schválení: kontrakt se mergne do main                   │
└─────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│  KROK 4 — Ruční vložení do Dawiso (žádná API integrace)     │
│                                                             │
│  STEP 1 — Data Product karta                                │
│    Dawiso > Data Catalog > Data Products > + New Product    │
│    Zkopíruj z x-dawiso.data_product: název, domain,        │
│    vlastníci, status, tagy, lineage, KO rules, retention    │
│                                                             │
│  STEP 2 — Business Glossary záznam (provede Data Steward)   │
│    Dawiso > Business Glossary > + New Term                  │
│    Zkopíruj z x-dawiso.glossary_entry: term, definition,   │
│    FIBO třída, domain, steward, synonyma, capability        │
└─────────────────────────────────────────────────────────────┘
```

### Co AI vygeneruje automaticky

Z tvého krátkého popisu AI:

| Co AI udělá | Jak |
|-------------|-----|
| Vybere správný název | Pravidlo `[Domain] [Concept] [Context] [Suffix]` |
| Přeloží české pojmy | Povinný překladový slovník |
| Zvolí Product Type | EVENT / STATE / AGGREGATION |
| Označí PII pole + sensitivity | `x-compliance` na každém poli schématu |
| Přiřadí Regulatory Framework | GDPR / BCBS 239 / IFRS 9 / None dle povahy dat |
| Vyplní FIBO třídu | Alignment na finanční ontologii |
| Připraví metadata pro Dawiso | Sekce `x-dawiso` — pro ruční vložení do UI |
| Navrhne schema tabulky | Standardní pole + business pole z popisu |
| Nastaví quality rules | Základní pravidla + row_count pro detekci anomálií |
| Vyplní SLA | Z popisu nebo defaulty (99.5%, D+1, 36 měsíců) |

### Jak použít AI prompt

**Krok 1:** Otevři soubor [`_template/prompt_contract_generator.md`](_template/prompt_contract_generator.md)

**Krok 2:** Zkopíruj celý obsah souboru a vlož ho do Claude (claude.ai)

**Krok 3:** Na konec promptu doplň odpovědi na tyto otázky (česky nebo anglicky):

```
[TEAM NAME / NUMBER]:         Tým 3 – Customer Service
[DOMAIN / BUSINESS AREA]:     Zákaznický servis, call centrum
[CONTACT PERSON + EMAIL]:     Jana Nováková, jana.novakova@nova-banka.cz
[CO PRODUKT OBSAHUJE]:        Záznamy o interakcích zákazníků – hovory,
                              chaty, emaily. Každý řádek = jedna interakce.
[KDO TO BUDE POUŽÍVAT]:       Call centrum, CRM systém, management CS
[ODKUD DATA POCHÁZEJÍ]:       CRM systém, telefonní ústředna
[KLÍČOVÁ DATOVÁ POLE]:        ID zákazníka, typ kanálu, délka interakce,
                              výsledek, datum, agent ID
[KVALITATIVNÍ POŽADAVKY]:     Délka interakce musí být > 0
[DATA LATENCY]:               D+1
[RETENTION]:                  36 měsíců
```

**Krok 4:** Claude vrátí hotový YAML soubor. Zkopíruj ho do složky svého týmu.

### Příklad vstupu a výstupu

**Vstup (30 sekund práce):**
```
[TEAM]: Tým 3
[DOMAIN]: zákaznický servis
[CO]: Záznamy o interakcích zákazníků s bankou (hovory, chaty)
[KDO POUŽÍVÁ]: Call centrum, CRM
[ODKUD]: CRM systém, telefonní ústředna
[POLE]: customer_id, channel_type, duration_seconds, outcome, agent_id
[LATENCY]: D+1
```

**Výstup (AI vygeneruje):**
- Název: `Customer Service Interaction History`
- Soubor: `customer-service-interaction-history.yml`
- FIBO: `fibo-fnd-pty-pty:Party`
- Dawiso Data Product + Glossary entry — vše vyplněno

> **Tip:** Čím více informací do vstupu napíšeš (pole, zdroje, use cases),
> tím méně budeš muset výstup ručně doplňovat.

---

## 9. Ukázka Data Contractu v YAML

> **Kompletní šablona se všemi sekcemi a komentáři je uložena v:**
> [`_template/datacontract_template.yml`](_template/datacontract_template.yml)
>
> Zkopíruj tento soubor do složky svého týmu, přejmenuj ho a vyplň hodnoty.

### Konvence pojmenování (Naming Convention)

Název data produktu se řídí strukturou: **[Domain] [Concept] [Context] [Suffix]**

| Složka | Popis | Příklady |
|--------|-------|---------|
| **Domain** | Obchodní doména (kontrolovaný slovník) | `Retail Sales` · `Customer Service` · `Accounting` · `Credit Risk` · `ESG Risk` · `Investment` · `Strategy` |
| **Concept** | Hlavní business entita (podstatné jméno) | `Customer` · `Account` · `Credit Memo` · `GL Account` · `KPI` |
| **Context** | Volitelné upřesnění (jen pokud je nutné odlišení) | `Acquisition` · `Underwriting` · `Energy` |
| **Suffix** | Typ produktu (EVENT / STATE / AGGREGATION) | EVENT → `History` `Log` `Events` · STATE → `Profile` `Snapshot` `Balances` · AGGREGATION → `Aggregation` `Performance` `Income` |

**Příklady platných názvů:**
```
Retail Sales Customer Acquisition History     (5 slov ✓)
Customer Service Interaction Performance      (4 slova ✓)
Accounting GL Account Balances                (4 slova ✓)
Credit Risk Credit Memo History               (5 slov ✓)
ESG Risk Building Energy Profile              (5 slov ✓)
Strategy KPI Aggregation                      (3 slova ✓)
```

---

### Minimální příklad (Strategy KPI Aggregation)

```yaml
dataContractSpecification: 1.1.0

id: urn:businessdomain:nova-banka:strategy:kpi-aggregation

info:
  title: DP_STRATEGY_KPI_AGGREGATION
  name: Strategy KPI Aggregation
  product_type: AGGREGATION
  maturity_score: 60%
  version: 1.0.0
  status: in development

  description: |
    Data product aggregating monthly strategic KPIs for board-level performance management.
    Data latency: D+1

    Business Entity:  KPI
    Business Purpose: Provide pre-computed KPI roll-ups for strategic decision-making.
    Consumers:        Strategy team, Board reporting
    Data Sources:     Core Banking System, Finance GL

    Filter Rules:
    * Only records with valid business_date
    * Region must be CZ or SK

    Use Cases:
    * UC1 - Monthly strategic KPI tracking
    * UC2 - Cross-business-unit performance comparison

  x-regulatory:
    gdpr_relevant: false
    critical_data_element: true
    regulatory_framework: "BCBS 239"

  owner: Nova Banka \ Team6 \ Strategy
  contact:
    name: Jan Novák
    email: jan.novak@nova-banka.cz

servers:
  PRODUCTION:
    type: databricks
    host: nova-banka-prod.cloud.databricks.com
    environment: production
    catalog: datamesh-nova-banka-prod
    schema: strategy-prod
    table: dp_strategy_kpi_aggregation

  DEVELOPMENT:
    type: databricks
    host: nova-banka-dev.cloud.databricks.com
    environment: development
    catalog: datamesh-nova-banka-dev
    schema: strategy-dev
    table: dp_strategy_kpi_aggregation

schema:
  - name: dp_strategy_kpi_aggregation
    description: Monthly KPI aggregation table for strategic reporting
    fields:

      - name: record_id
        type: string
        description: Unique record identifier (UUID)
        required: true
        unique: true
        example: "550e8400-e29b-41d4-a716-446655440000"
        x-compliance:
          is_pii: false
          sensitivity: Internal

      - name: business_date
        type: date
        description: Business date of the record (YYYY-MM-DD)
        required: true
        example: "2024-01-31"
        x-compliance:
          is_pii: false
          sensitivity: Internal

      - name: region
        type: string
        description: Geographic region — allowed values CZ or SK
        required: true
        enum: [CZ, SK]
        example: "CZ"
        x-compliance:
          is_pii: false
          sensitivity: Internal

      - name: kpi_name
        type: string
        description: KPI indicator name
        required: true
        example: "Net_Interest_Margin"
        x-compliance:
          is_pii: false
          sensitivity: Internal

      - name: kpi_value
        type: decimal
        description: KPI indicator value
        required: true
        example: 2.35
        x-compliance:
          is_pii: false
          sensitivity: Internal

      - name: kpi_target
        type: decimal
        description: Target value for the KPI
        required: false
        example: 2.50
        x-compliance:
          is_pii: false
          sensitivity: Internal

      - name: currency
        type: string
        description: Currency code (ISO 4217)
        required: false
        example: "CZK"
        x-compliance:
          is_pii: false
          sensitivity: Internal

      - name: created_at
        type: timestamp
        description: Record creation timestamp (UTC)
        required: true
        example: "2024-01-31T08:00:00Z"
        x-compliance:
          is_pii: false
          sensitivity: Internal

      - name: updated_at
        type: timestamp
        description: Record last update timestamp (UTC)
        required: true
        example: "2024-01-31T08:00:00Z"
        x-compliance:
          is_pii: false
          sensitivity: Internal

quality:
  - rule: not_null
    field: record_id
    description: Record ID must not be empty

  - rule: unique
    field: record_id
    description: Every record must have a unique ID

  - rule: not_null
    field: business_date
    description: Business date must not be empty

  - rule: accepted_values
    field: region
    values: [CZ, SK]
    description: Region must be CZ or SK

  - rule: not_null
    field: kpi_value
    description: KPI value must not be empty

  - rule: row_count
    min: 100
    max: 10000
    description: Detects data distribution anomalies (volume drop/spike)

sla:
  availability: 99.5%
  data_latency: D+1
  retention_period: 36 months
  support_contact: jan.novak@nova-banka.cz
```

---

## 10. Časté chyby a jak je opravit

### ❌ "Merging is blocked"
**Příčina:** Pull Request nemá požadované schválení.
**Řešení:** Požádej kolegu z tvého týmu aby PR schválil.

### ❌ Commitoval jsem přímo do `main`
**Příčina:** Nezvolil jsi vlastní branch před commitem.
**Řešení:** Vytvoř novou branch, přenes změny a otevři PR. Požádej správce o pomoc.

### ❌ Nahrál jsem soubor do špatné složky
**Příčina:** Nebyl jsi ve složce svého týmu.
**Řešení:** Smaž soubor ze špatné složky, nahraj ho do správné a vytvoř PR.

### ❌ YAML soubor má chybu ve formátování
**Příčina:** YAML je citlivý na odsazení (mezery).
**Řešení:** Použij online validátor na [yamllint.com](https://www.yamllint.com) před nahráním.

---

## 💬 Kde najdeš šablony a prompty

| Soubor | K čemu slouží |
|--------|---------------|
| [`_template/datacontract_template.yml`](_template/datacontract_template.yml) | Kompletní šablona se všemi sekcemi a komentáři |
| [`_template/prompt_contract_generator.md`](_template/prompt_contract_generator.md) | AI prompt — vygeneruje celý YAML z krátkého popisu |

---

## 💬 Potřebuješ pomoct?

Kontaktuj správce repozitáře nebo otevři **Issue** v repozitáři:
1. Klikni na záložku **"Issues"**
2. Klikni **"New issue"**
3. Popiš svůj problém

---

*Dokument vytvořen pro školní projekt Nova Banka — Data Mesh repozitář.*
