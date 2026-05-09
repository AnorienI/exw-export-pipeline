EXW to FCA (and FAS) Pipeline
A data-driven pipeline for modeling the cost and compliance shift from EXW to FCA/FAS for Brazilian exporters.

Overview
Selling under EXW (Ex Works) in Brazil can expose small producers to tax liability if the export is not properly registered in Siscomex (DU-E).

This project combines:

A legal-operational model for export intermediation.

A data pipeline that quantifies the cost difference between EXW and FCA/FAS.

The goal is to provide a reproducible and transparent framework for export decision-making.

Key Features
Deterministic cost modeling (EXW → FCA/FAS).

Structured data ingestion (freight tables, distance matrices).

MariaDB-backed relational schema.

Modular pipeline design (ingestion → normalization → computation → output).

Designed for reproducibility and extension.

Project Structure
Plaintext
exw-fca-pipeline/
├── data/           # Raw and processed datasets
├── scripts/        # Python scripts (ETL, calculations)
├── sql/            # Schema and queries (schema.sql)
├── output/         # Generated reports / comparisons
├── .env.example    # Template for environment variables
├── README.md
└── requirements.txt
Technical Architecture
Pipeline Stages
Ingestion: Freight tables and IBGE distance data.

Normalization: Unit standardization (kg, ton) and Incoterm scope alignment.

Cost and Risk Engine: Computes price delta and encodes logistics/compliance assumptions.

Output Layer: Comparative cost tables and decision-support outputs.

Database Schema
The project uses MariaDB with the following core tables:

products: NCM codes and physical attributes.

origins: Production locations.

ports: Export terminals.

freight_matrix: Distance-based transport costs.

Getting Started
1. Clone the repository
Bash
git clone https://github.com/AnorienI/exw-fca-pipeline.git
cd exw-fca-pipeline
2. Configure Environment Variables
The project uses a .env file to manage database credentials safely.

Copy the example file: cp .env.example .env

Open .env and fill in your local MariaDB credentials:

Plaintext
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=exw_fca
3. Set up the Database
Bash
mysql -u your_user -p < sql/schema.sql
4. Install Dependencies
Bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mint
pip install -r requirements.txt
5. Run the Pipeline
Bash
python3 scripts/main.py
Example Output
The pipeline produces structured comparisons, including:

Transport cost adjustments.

Export handling costs.

Final adjusted price estimates.

(Add a sample CSV or screenshot here later — this is very valuable for recruiters.)

Use Case
Designed for:

Small and medium Brazilian producers.

Export consultants and trade intermediaries.

Data-driven logistics analysis.

Roadmap
Add visualization layer (charts / dashboards).

Integrate real-time freight APIs.

Expand Incoterms coverage.

Improve cost modeling granularity.

License
[Insert License Type]

Author: Anestis Mystakidis