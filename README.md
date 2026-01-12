# REPO-CHIE: Data Engineering Internship (Week 1)

## Project Overview
This repository contains the Week 1 deliverables for the Data Engineering Internship. The core objective was to build a robust ETL (Extract, Transform, Load) pipeline that handles web-based data ingestion while ensuring strict data types and schema consistency.

## Tech Stack
* **Environment:** WSL2 (Ubuntu 24.04)
* **Language:** Python 3.12
* **Libraries:** Requests, BeautifulSoup4 (lxml), Pandas
* **Version Control:** Git

## Pipeline Logic
1. **Extract:** Utilizes the `requests` library with defined timeouts to pull raw HTML.
2. **Transform:** Uses `BeautifulSoup` with the `lxml` parser to isolate data points, followed by `Pandas` for schema enforcement and timestamping.
3. **Load:** Persists the cleaned dataset to a flat-file (CSV) landing zone.

## How to Run
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python etl_pipeline.py
# REPO-CHIE
Data Ingestion Pipeline (Week 1)   Intern Ref ID: ICP-IX8D2E-2026. A production-ready ETL scraper built with Python, Pandas, and BeautifulSoup. Implements automated extraction, data cleaning for format consistency, and localized loading to CSV.
