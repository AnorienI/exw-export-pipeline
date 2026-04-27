EXW to FCA (and FAS) Pipeline

A data-driven pipeline for modeling the cost and compliance shift from EXW to FCA/FAS for Brazilian exporters.

Overview

Selling under EXW (Ex Works) in Brazil can expose small producers to tax liability if the export is not properly registered in Siscomex (DU-E).

This project combines:

A legal-operational model for export intermediation
A data pipeline that quantifies the cost difference between EXW and FCA/FAS

The goal is to provide a reproducible and transparent framework for export decision-making.

Key Features
Deterministic cost modeling (EXW → FCA/FAS)
Structured data ingestion (freight tables, distance matrices)
MariaDB-backed relational schema
Modular pipeline design (ingestion → normalization → computation → output)
Designed for reproducibility and extension
Project Structure
exw-fca-pipeline/
├── data/                # Raw and processed datasets
├── scripts/             # Python scripts (ETL, calculations)
├── sql/                 # Schema and queries
├── output/              # Generated reports / comparisons
├── README.md
└── requirements.txt
Technical Architecture
Pipeline Stages
Ingestion
Freight tables
IBGE distance data
Normalization
Unit standardization (kg, ton)
Incoterm scope alignment
Cost and Risk Engine
Computes price delta between EXW and FCA/FAS
Encodes logistics and compliance assumptions
Output Layer
Comparative cost tables
Decision-support outputs
Database Schema

The project uses MariaDB with the following core tables:

products — NCM codes and physical attributes
origins — production locations
ports — export terminals
freight_matrix — distance-based transport costs
Getting Started
1. Clone the repository
git clone https://github.com/anorien/exw-fca-pipeline.git
cd exw-fca-pipeline
2. Set up the database
mysql -u your_user -p < sql/schema.sql
3. Install dependencies
pip install -r requirements.txt
4. Run the pipeline
python scripts/main.py
Example Output

The pipeline produces structured comparisons between EXW and FCA/FAS pricing, including:

Transport cost adjustments
Export handling costs
Final adjusted price estimates

(Add a sample CSV or screenshot here later — this is very valuable for recruiters.)

Use Case

Designed for:

Small and medium Brazilian producers
Export consultants and trade intermediaries
Data-driven logistics analysis
Roadmap
Add visualization layer (charts / dashboards)
Integrate real-time freight APIs
Expand Incoterms coverage
Improve cost modeling granularity

License

 (e.g., MIT).

 Author 

 Anestis Mystakidis