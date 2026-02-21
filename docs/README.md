# Project Documentation

Welcome to the P2C-Stack documentation.

## Contents

- **[Frontend Components](FRONTEND_COMPONENTS.md)**: Detailed guide to the React components in `p2cfrontend`.
- **[Backend Components](BACKEND_COMPONENTS.md)**: Overview of the legacy `p2cproxy` middleware.
- **[Database Schema](DB-Schema.md)**: Information about the SQL Server database schema, including the updated `row_hash` UUID identity constraint.
- **[Data API (`ScalableMssqlApi`)](../ScalableMssqlApi/API_DOCUMENTATION.md)**: Deep-dive into the C# REST endpoints manipulating the Database.
- **[Orchestrator & Ingestion Pipelines](../P2CScripts/docs/P2C_ORCHESTRATOR.md)**: Documentation for the Dockerized UI, FastAPI backend, dynamic proxy pooling, and the Python ETL post-processing system.

## Quick Start

1.  **Start the Stack**:
    ```bash
    docker compose up --build
    ```
2.  **Access the Application**:
    - Frontend: [http://localhost:8004](http://localhost:8004)
    - Proxy: [http://localhost:9000](http://localhost:9000)
    - API: [http://localhost:8083](http://localhost:8083)
