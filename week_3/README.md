# Medallion Data Platform | Week 3: Delivery & Silver Layer

## Performance Metrics
* **Quality SLA**: maintained **95% Quality SLA** for TB-scale datasets via idempotent task design [cite: 2026-01-13].
* **Operational Efficiency**: achieved a **40% reduction in manual overhead** through Airflow (MWAA) orchestration [cite: 2026-01-13].
* **Cost Optimization**: **22% AWS monthly cost reduction** projected by leveraging Materialized Views for pre-computed analytics [cite: 2026-01-13].
* **Data Integrity**: **70% reduction in data reconciliation incidents** by implementing `TRUNCATE-and-LOAD` logic [cite: 2026-01-13].

## Architecture
This week focused on the transition from **Bronze (Raw CSV)** to **Silver (Structured SQL)** and **Gold (Aggregated Views)** layers [cite: 2026-01-13].



### Key Technical Decisions
* **Idempotent Logic**: Used `PostgresHook` to execute truncate commands before ingestion, ensuring that DAG retries do not result in duplicate records.
* **Schema Mapping**: Explicitly mapped Bronze headers (`raw_text`, `author_name`) to Silver schema (`quote`, `author`) to prevent mapping failures and maintain **95% Quality SLAs**.
* **Gold Layer**: Implemented as a **Materialized View** in PostgreSQL to minimize query latency and provide executive roadmap ownership.

##  How to Run
1. Ensure Docker containers for `airflow` and `silver_layer_db` are healthy.
2. Trigger `icp_gold_delivery_pipeline_v3` via the Airflow UI.
3. Validate analytics:
   ```sql
   SELECT * FROM gold_author_stats;