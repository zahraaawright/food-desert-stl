# St. Louis food desert analysis

Revisits an old college project (grocery vs. dollar store density in St. Louis)
with a proper stack: Pulumi (TypeScript) on GCP, Airflow, BigQuery, dbt, and a
Streamlit dashboard.

## Layout
- `infra/` – Pulumi TypeScript program that provisions the GCS bucket and BigQuery dataset
- `ingestion/` – Python scripts that pull from the Google Places API and Census ACS API
- `dbt/` – transforms raw tables into modeled food-desert scores
- `airflow/` – DAG that runs ingestion then triggers dbt
- `dashboard/` – Streamlit app for non-technical viewers
- `.github/workflows/` – CI that runs `pulumi preview` on pull requests

## Quick start
See the setup steps in the chat this was generated from, or roughly:
1. `cd infra && npm install && pulumi up`
2. Set `GOOGLE_PLACES_API_KEY` and `CENSUS_API_KEY` env vars, run the ingestion scripts once
3. `cd dbt && dbt run`
4. `cd dashboard && streamlit run app.py`
