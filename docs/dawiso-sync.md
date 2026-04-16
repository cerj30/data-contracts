# Dawiso Sync

Repo uz obsahuje automaticky krok, ktory sa spusti po uspesnej validacii kontraktov na `push` do `main`.

## Co sa deje

Workflow `validate-contracts.yml` teraz robi 2 veci:

1. validuje vsetky datove kontrakty ako doteraz
2. po uspesnej validacii spusti `.github/scripts/sync_dawiso.py`

Sync skript:

- vezme iba zmenene `*.yml` a `*.yaml` kontrakty z aktualneho pushu
- premapuje ich na stabilny JSON payload
- priradi kazdemu kontraktu cielovy Dawiso team podla nazvu priecinka
- rozlisi `upserts` a `deletes`
- payload ulozi do `dawiso_payload.json`
- volitelne payload posle na Dawiso API endpoint

## Team mapping

Aktualne mapovanie priecinkov na Dawiso timy:

- `team1-digi` -> `Team - Digi Prodej`
- `team2-Data-Governance` -> `Team - Data Governance &EA`
- `team3-client-service` -> `Team - Obsluha klienta`
- `team4-steering-data` -> `Team - Steering Data`
- `team5-esg-risk` -> `Team - Risk ESG`
- `team6-strategy` -> `Team - Strategy`
- `team7-gen-ai` -> `Team - ICM Gen AI`
- `team8-investment-banking` -> `Team - Investment Banking`

## Potrebne nastavenie v GitHube

### Secrets

- `DAWISO_API_URL`
- `DAWISO_API_TOKEN`

### Repository Variables

- `DAWISO_SYNC_MODE`
  - `export`: vytvori iba artifact `dawiso-payload`
  - `api`: posle payload na `DAWISO_API_URL`
- `DAWISO_TIMEOUT_SECONDS`
  - volitelne, default je `30`

## Odporucany rollout

1. nastavte `DAWISO_SYNC_MODE=export`
2. pushnite testovaciu zmenu kontraktu do `main`
3. skontrolujte artifact `dawiso-payload`
4. pripravte v Dawise endpoint, ktory vie spracovat `upserts` a `deletes`
5. doplnte `DAWISO_API_URL`, `DAWISO_API_TOKEN`
6. prepnite `DAWISO_SYNC_MODE=api`

## Tvar payloadu

Skript posiela JSON v tvare:

```json
{
  "generated_at_utc": "2026-04-16T14:30:00+00:00",
  "repository": "org/data-contracts",
  "branch": "main",
  "commit": "abc123",
  "upserts": [
    {
      "contract_path": "team3-client-service/customer_service_customer_profile_data_contract.yaml",
      "contract_id": "urn:...",
      "title": "Customer Service Customer Profile",
      "domain": "Client Service",
      "product_owner": "Name",
      "data_steward": "Name",
      "databricks_paths": [
        "PRODUCTION:catalog.schema.table"
      ],
      "field_count": 12,
      "pii_field_count": 2,
      "pii_share": 0.1667
    }
  ],
  "deletes": [
    "team1-digi/old_contract.yaml"
  ]
}
```

## Dolezita poznamka

ChatGPT connector do Dawisa je super na manualnu obsluhu, ale na automatizaciu je lepsie ist system-to-system integraciou:

- GitHub Actions ako trigger
- service account / token pre Dawiso
- stabilny API payload namiesto promptu

To je spolahlivejsie, auditovatelnejsie a lahsie spravovatelne.
