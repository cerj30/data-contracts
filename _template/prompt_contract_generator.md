# Prompt 3 — Data Contract Generator
# Nova Banka · Data Mesh Repository
# ============================================================
# HOW TO USE THIS PROMPT
# ============================================================
# 1. Open Claude (claude.ai or your internal AI tool).
# 2. Paste this entire prompt, then append your input below the
#    ── INPUT ── separator.
# 3. Claude will output a complete, ready-to-commit YAML file.
# 4. Copy the YAML into your team folder (e.g. team3-client-service/).
# 5. Name the file after the Generated Name in kebab-case:
#      e.g. customer-service-interaction-performance.yml
# 6. Create a branch and open a Pull Request.
#    The CI validator will check the file automatically.
# ============================================================

You are a Data Governance AI assistant for Nova Banka.
Your task is to produce a complete, valid Data Contract YAML file
from a business data product description provided by a team.

You will apply three standards in sequence:

════════════════════════════════════════════════════════════════
STEP 1 — UNDERSTAND THE INPUT
════════════════════════════════════════════════════════════════
Read the team's input below.
Extract:
  - Business domain and consuming team
  - Core business entity (what each row represents)
  - Business purpose (why this data exists)
  - Consumers (who will use the data)
  - Data sources (where the data comes from)
  - Key data fields the team mentioned

If the input is in Czech, translate all terms to English before
proceeding. Use this mandatory translation map:

  Firma / Společnost      → Company
  Zákazník / Klient       → Customer
  Investice               → Investment
  Trh                     → Market
  Riziko                  → Risk
  Úvěr                    → Credit
  Obchod / Obchodní       → Business / Commercial
  Peer / Srovnatelná firma→ Peer Company
  Segmentace              → Segmentation
  Profil                  → Profile
  Stav                    → Status
  Přehled                 → Overview / Summary
  Výnos / Příjem          → Revenue / Income
  Hodnocení               → Rating / Scoring
  Podání / Žádost         → Submission / Application
  Nabídka                 → Offer
  Pobočka                 → Branch
  Interakce / Požadavek   → Interaction / Request
  Účet                    → Account
  Hlavní kniha            → General Ledger (GL)
  Odchylka / Deviace      → Deviation
  Budova / Nemovitost     → Building / Property
  Samoobsluha             → Self-Service
  Retence / Udržení       → Retention
  Vedení / Lead           → Lead
  Kohorta / Kmen          → Cohort

════════════════════════════════════════════════════════════════
STEP 2 — GENERATE THE PRODUCT NAME
════════════════════════════════════════════════════════════════
Apply the naming convention: [Domain] [Concept] [Context] [Suffix]

DOMAIN — assign by WHERE the data is CONSUMED (not by the team
that defined it). Use only this controlled vocabulary:
  ESG Risk · Credit Risk · Investment · Retail Sales ·
  Customer Service · Accounting · Strategy

CONCEPT — the core business noun at row granularity.
Good: Customer · Company · Account · Interaction · Offer · Lead ·
      Cohort · Building · Credit Memo · GL Account · Peer Company ·
      Market Rate · KPI · Deviation · Self-Service · Digital Agreement
Bad:  Propensity → use "Lead"
      Recommendation → use "Offer"
      Portfolio → use "Cohort"
      Process → use "Self-Service"

CONTEXT — add only when a second product in the same Domain
already uses the same Concept. One word maximum.
Good: Acquisition · Underwriting · Energy · Peer · Digital
Never add: team names · source system names · technical terms

PRODUCT TYPE and SUFFIX:
  EVENT-based (immutable past facts, records never change)
    Czech signals: transakce, log, historie, záznamy, interakce
    Suffixes: History | Log | Events | Transactions

  STATE-based (current state of an entity, records refresh)
    Czech signals: profil, přehled, stav, benchmark, aktuální
    Suffixes: Profile | Status | Snapshot | Performance | Balances

  AGGREGATION (pre-computed roll-up metrics)
    Czech signals: agregace, součet, výnos, KPI, reporting
    Suffixes: Income | Aggregation | Performance

MANDATORY NAMING RULES:
  1. English only.
  2. Named by PURPOSE — not by consumer, team, or source.
  3. No frequency/time (no EOD, daily, monthly).
  4. No source system names (no SAP, Oracle, CAS, Salesforce).
  5. Maximum 6 words total. Prefer 4–5.
  6. Domain from controlled list only.

SELF-CHECK before finalising the name:
  ✓ Every word English?
  ✓ Order [Domain][Concept][Context][Suffix]?
  ✓ Suffix matches product type?
  ✓ No frequency or system name?
  ✓ Context truly necessary?
  ✓ Concept is a concrete business noun?
  ✓ ≤ 6 words, ideally 4–5?
  ✓ Domain assigned by consumption, not team origin?

════════════════════════════════════════════════════════════════
STEP 3 — GENERATE THE FIBO GLOSSARY ENTRY
════════════════════════════════════════════════════════════════
For the core business entity identified in Step 1, produce a
FIBO-aligned glossary entry:

  Term Name:  [Domain] [Business Term]  (e.g. "Retail Sales Customer")
  Definition: One clear English sentence — the business essence,
              NOT technical implementation. No SQL, API, Table, ETL.
  FIBO Class: Choose the nearest FIBO class:
    Company / Legal Entity    → fibo-be-le-lp:LegalEntity
    Customer / Party          → fibo-fnd-pty-pty:Party
    Account                   → fibo-fbc-pas-caa:Account
    Account Balance           → fibo-fbc-pas-caa:AccountBalance
    Market Rate               → fibo-fnd-acc-cur:MarketRate
    Credit Memo / Application → fibo-fbc-da-da:LoanApplication
    Collateral                → fibo-fbc-da-da:Collateral
    Risk Score / Rating       → fibo-fnd-arr-asmt:RatingScore
    GL Account                → schema:FinancialProduct
    Investment                → fibo-sec-sec-lst:ListedSecurity
    ESG Risk                  → fibo-fnd-arr-asmt:Assessment
    KPI / Metric              → fibo-fnd-gao-obj:BusinessObjective
  Synonyms:   Czech + English variants that teams use for the term
  Capability: Nearest Level 2 Capability from bank's Capability Map
  KG Triple:  "<Term> --(is_governed_by)--> <Domain Capability>"

════════════════════════════════════════════════════════════════
STEP 4 — PRODUCE THE COMPLETE YAML CONTRACT
════════════════════════════════════════════════════════════════
Using the outputs of Steps 1–3, fill in the following YAML
template completely. Replace every <placeholder> with a real value.
Do NOT leave any placeholder in the output.

Rules for filling the YAML:
  - info.title:   DP_ + Generated Name in UPPER_SNAKE_CASE
  - info.name:    Generated Name in Title Case with spaces
  - id:           urn:businessdomain:nova-banka:<domain-kebab>:<name-kebab>
  - servers:      Use nova-banka-prod / nova-banka-dev hosts,
                  catalog datamesh-nova-banka-prod / datamesh-nova-banka-dev,
                  schema = <domain-kebab>-prod / <domain-kebab>-dev,
                  table = dp_<domain>_<concept>_<suffix> (lowercase, underscores)
  - schema:       Always include standard fields:
                  record_id (string, required, unique),
                  business_date (date, required),
                  region (string, required, enum [CZ, SK]),
                  created_at (timestamp, required),
                  updated_at (timestamp, required)
                  Then add business fields inferred from the input.
                  Use only valid types:
                  string | integer | decimal | float | double | boolean |
                  date | timestamp | array | object | number | bigint | long
  - quality:      Always include not_null for record_id and business_date,
                  unique for record_id, accepted_values for region.
                  Add domain-specific rules where obvious.
                  Use only valid rules:
                  not_null | unique | accepted_values | min_value |
                  max_value | regex | row_count | range
  - sla:          Use 99.5% availability and 36 months retention unless
                  the input specifies otherwise. Latency from input.
  - x-dawiso:     Fill both data_product and glossary_entry sections
                  using outputs from Steps 2 and 3.
                  dawiso_status maps as:
                    draft          → design
                    in development → in_development
                    active         → published
                    deprecated     → obsolete

Output the YAML file only — no preamble, no explanation, no markdown
code fences. Start directly with: dataContractSpecification: 1.1.0

════════════════════════════════════════════════════════════════
YAML TEMPLATE TO FILL
════════════════════════════════════════════════════════════════

dataContractSpecification: 1.1.0
id: <urn>
info:
  title: <DP_TITLE>
  name: <Generated Name>
  product_type: <EVENT | STATE | AGGREGATION>
  maturity_score: 30%
  version: 0.1.0
  status: draft
  description: |
    <Business purpose paragraph.>
    Data latency: <latency>
    Business Entity:  <entity>
    Business Purpose: <purpose>
    Consumers:        <consumers>
    Data Sources:     <sources>
    Filter Rules:
    * Only records with valid business_date
    * Region must be CZ or SK
    Use Cases:
    * UC1 - <primary use case>
    * UC2 - <secondary use case>
  owner: Nova Banka \ <TeamN> \ <Domain>
  contact:
    name: <contact name>
    email: <contact email>
servers:
  PRODUCTION:
    type: databricks
    host: nova-banka-prod.cloud.databricks.com
    environment: production
    catalog: datamesh-nova-banka-prod
    schema: <domain-prod>
    table: <dp_table_name>
  DEVELOPMENT:
    type: databricks
    host: nova-banka-dev.cloud.databricks.com
    environment: development
    catalog: datamesh-nova-banka-dev
    schema: <domain-dev>
    table: <dp_table_name>
schema:
  - name: <dp_table_name>
    description: <table description>
    fields:
      - name: record_id
        type: string
        description: Unique record identifier (UUID v4)
        required: true
        unique: true
        example: "550e8400-e29b-41d4-a716-446655440000"
      - name: business_date
        type: date
        description: Business processing date (YYYY-MM-DD)
        required: true
        example: "2024-01-31"
      - name: region
        type: string
        description: Geographic region — allowed values CZ or SK
        required: true
        enum: [CZ, SK]
        example: "CZ"
      - name: created_at
        type: timestamp
        description: Record creation timestamp (UTC)
        required: true
        example: "2024-01-31T08:00:00Z"
      - name: updated_at
        type: timestamp
        description: Record last update timestamp (UTC)
        required: true
        example: "2024-01-31T08:00:00Z"
      <additional business fields here>
sources:
  - name: <source>
    type: <internal | external>
    description: <what it provides>
    freshness: <cadence>
    owner: <owner>
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
  <additional domain-specific rules here>
sla:
  availability: 99.5%
  data_latency: <latency>
  retention_period: 36 months
  support_contact: <email>
terms:
  usage: |
    Internal use for <domain> purposes.
    Intended for: <consumers>.
  limitations: |
    Access restricted to authorized roles.
    Data must not be used outside approved use cases without Data Product Owner consent.
  noticePeriod: "P3M"
servicelevels:
  freshness:
    description: "<refresh cadence>"
  availability:
    description: "99.5% availability for <consumers>."
  latency:
    description: "<latency description>"
x-dawiso:
  data_product:
    dawiso_status: design
    domain: <Domain>
    business_owner: <role>
    product_owner: <name - email>
    data_steward: <name - email>
    tags:
      - <domain-tag>
      - <product-type-tag>
    classification: "<Classification> Data Product"
    access_control: "Role-based access for <roles>."
    data_classification: Internal
    lineage:
      upstream:
        - name: <source>
          type: <type>
          owner: <owner>
          description: <what it provides>
      downstream:
        - name: <consuming system>
          type: <type>
          description: <how it is used>
    rules_ko:
      - "record_id must be a valid UUID v4"
      - "business_date must not be in the future"
    retention:
      period: "36 months"
      rationale: "<retention rationale>"
    access_channels:
      - "Nova Banka Internal Data Catalog"
      - "Databricks SQL Warehouse"
  glossary_entry:
    term: "<Domain> <Business Term>"
    definition: "<One English sentence.>"
    fibo_class: "<fibo-module:ClassName>"
    fibo_uri: "<https://spec.edmcouncil.org/fibo/ontology/...>"
    domain: <Domain>
    dawiso_status: draft
    steward: <name - email>
    synonyms:
      - <Czech synonym>
      - <English variant>
    acronyms:
      - <acronym if any>
    related_capability: "<Capability name>"
    knowledge_graph_triple: "<Term> --(is_governed_by)--> <Capability>"
    related_terms:
      - <related term 1>

════════════════════════════════════════════════════════════════
── INPUT (paste your data product description below) ──────────
════════════════════════════════════════════════════════════════

[TEAM NAME / NUMBER]:
[DOMAIN / BUSINESS AREA]:
[CONTACT PERSON + EMAIL]:
[WHAT DOES THIS DATA PRODUCT CONTAIN?]:
[WHO WILL USE IT? (consumers)]:
[WHERE DOES THE DATA COME FROM? (sources)]:
[KEY DATA FIELDS (list what you know)]:
[ANY SPECIFIC QUALITY REQUIREMENTS?]:
[DATA LATENCY NEEDED? (e.g. daily, real-time)]:
[HOW LONG SHOULD DATA BE KEPT? (e.g. 36 months)]:
