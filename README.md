# ✈️ U.S. Aviation Analytics (2010 – 2024)

> **Policy-driven data project** using BigQuery, Databricks (PySpark | Scala) and Python econometrics to uncover supply–demand mismatches, CARES Act impacts, rural-airport equity, ULCC market dynamics, and sentiment-driven strategy.

---

## 📑 Table of Contents

1. [Project Architecture](#project-architecture)
2. [Folder Layout](#folder-layout)
3. [Quick Start](#quick-start)
4. [Data Sources](#data-sources)
5. [Analytical Modules](#analytical-modules)
6. [Cloud & DevOps Details](#cloud--devops-details)
7. [Key Visualizations](#key-visualizations)
8. [Results & Strategic Insights](#results--strategic-insights)
9. [Road Map](#road-map)

---

## Project Architecture

![Architecture Diagram](plots/architecture.png)

````

## Folder Layout

```text
.
├── bigquery/                 # Production SQL scripts
├── cloud_run/                # Minimal REST wrapper (FastAPI) for metrics
├── databricks/               # Scala / PySpark notebooks or .dbc exports
├── data/
│   ├── raw/                  # Original DOT & FAA files
│   └── processed/            # Cleaned tables & model outputs
├── gcp_config/               # Helper scripts for auth & load
├── notebooks/                # Story notebooks (one per question)
├── plots/                    # PNGs used in README / report
├── scripts/
│   ├── etl/                  # Python merge helpers
│   ├── modeling/             # PanelOLS, elasticity, DiD
│   └── viz/                  # Matplotlib / seaborn helpers
├── sentiment_analysis/       # Dow Jones news pipeline
└── requirements.txt
````

## Quick Start

```bash
# 1️⃣  Create & activate env
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2️⃣  Authenticate to GCP
bash gcp_config/gcloud_auth.sh   # sets `GOOGLE_APPLICATION_CREDENTIALS`

# 3️⃣  Re-run BigQuery transforms (optional)
bq query --use_legacy_sql=false < bigquery/002_create_table_mismatch_index.sql

# 4️⃣  Launch notebooks
jupyter lab notebooks/
```

## Data Sources

| Dataset | Years | Size | Notes |
| --- | --- | --- | --- |
| DOT T-100 Domestic Segment | 2010-2024 Q1-Q4 | 1 GB | Seat-level capacity |
| DB1B 10 % Ticket Sample | 2010-2024 Q1-Q4 | 1.9 GB | Passenger & fare |
| ARP NPIAS 2025-2029 Appendix A | 2024 release | 5 MB | Airport classes |
| Dow Jones Factiva Aviation News (~ 7 Million articles) | 2000-2024 | 20GB | Sentiment shocks |

## Analytical Modules

| Business Question | Notebook | Tools Used & Source Code |
| --- | --- | --- |
| **Do airlines misalign seat supply and demand?** | `mismatch_anaylsis.ipynb` | BigQuery: `002_create_table_mismatch_index.sql`<br>Databricks: `mismatch_analysis.scala` |
| **Did the CARES Act restore load factors?** | `cares_analysis.ipynb` | BigQuery: `003_load_factor_compute.sql` |
| **Are non-hub (rural) airports losing capacity?** | `rural_trend_analysis.ipynb` | CSV Join: `classification_airports.csv` |
| **How do ULCCs differ in price & demand?** | `ulcc_legacy_analysis.ipynb` | In-notebook analysis using pandas/statsmodels |
| **Causal impact of ULCC entry (DiD)?** | `fare_elasticity_did.ipynb` | BigQuery: `004_create_DiD_table.sql` |
| **Do negative news shocks trigger capacity cuts?** | `sentiment_vs_defense_dowjones.ipynb` | BigQuery: `005_sentiment_shock_summary.sql` |
| **Which media themes influence airline strategy most?** | `themes_vs_ops.ipynb` | BERTopic, TF-IDF correlation, BigQuery + GCS |

See notebooks/ for fully reproducible analysis with inline comments.

## Cloud & DevOps Details

- BigQuery tables created with `write_to_bigquery.py`
- Databricks cluster JSON (autoscaling 2–8 r5.xlarge) at `databricks/cluster_config.json`
- CI/CD via GitHub Actions → runs `black`, `flake8`, and _dbt test_ stubs against staging BigQuery dataset
- Cloud Run (`cloud_run/`) optional micro-service returning JSON KPI endpoints (`/mismatch`, `/cares`, `/ulcc`)

## Key Visualizations

| PNG (store in plots/) | Purpose |
| --- | --- |
| mismatch_trend_area.png | Undersupply / oversupply stacked-area 2010-2024 |
| load_factor_over_time.png | Quarterly LF with CARES Act marker |
| rural_capacity_line.png | Seat totals by airport class |
| fare_elasticity_plot.png | Log-log fare vs passengers + regression lines |
| did_treatment_trend.png | Avg passengers (treated vs control) pre/post ULCC |
| topicthemes_vs_operations.png | Heatmap with descriptive BERTopic themes |
| architecture_diagram.png | High-level GCP + Databricks pipeline |
| bigquery_console_query.png | Example completed query in BigQuery UI |

## Results & Strategic Insights

Full statistical tables and interpretations live in the Aviation Analysis Report. Highlights:

- Chronic undersupply – up to 9.2 k routes mis-served in Q2 2013; still 5.4 k in 2024.
- CARES success – load factor +22 pp (p ≈ 0.07 OLS; p ≈ 0.03 Welch).
- Rural equity myth – no significant rural decline (p = 0.55); inequality root is distribution, not attrition.
- ULCC economics – 25 % cheaper fares; positive demand elasticity (+0.53).
- ULCC entry – +7.7 % causal passenger lift (p < 0.0001).
- Sentiment drag – legacy carriers cut 2.4 % seats after negative news (p = 0.014).

## Road Map

- Multivariate CARES model – add GDP, jet-fuel price, vax-rate controls
- GRU/LSTM forecasts – predict mismatch index with exogenous sentiment series
- Snowflake / BigLake benchmark – cross-cloud performance shoot-out
- Streamlit What-If app – interactive capacity-planning sandbox

---

## License

MIT – see LICENSE for details.
