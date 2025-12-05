# Project Documentation

Welcome to the P2C-Stack documentation.

## Contents

- **[Frontend Components](FRONTEND_COMPONENTS.md)**: Detailed guide to the React components in `p2cfrontend`.
- **[Backend Components](BACKEND_COMPONENTS.md)**: Overview of the `p2cproxy` and `p2capi` services.
- **[Database Schema](DB-Schema.md)**: Information about the SQL Server database schema.
- **[Data Ingestion Scripts](../P2CScripts/README.md)**: Documentation for the Python and PowerShell scripts used to scrape and ingest data.

## Quick Start

1.  **Start the Stack**:
    ```bash
    docker compose up --build
    ```
2.  **Access the Application**:
    - Frontend: [http://localhost:8004](http://localhost:8004)
    - Proxy: [http://localhost:9000](http://localhost:9000)
    - API: [http://localhost:8083](http://localhost:8083)
