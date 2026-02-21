# Docker Containers

This document lists all the containerized services that make up the P2C application stack.

## Service Overview

| Service Name | Image | Port (Host:Container) | Description |
| :--- | :--- | :--- | :--- |
| `p2cfrontend` | `p2cfrontend:latest` | `8004:80` | The React-based frontend application (Vite). Serves the UI. |
| `p2cproxy` | `p2cproxy:latest` | `9000:9000` | Node.js middleware. Handles auth, caching, geocoding, and proxies API requests. |
| `p2capi` | `p2capi:latest` | `8083:8083` | .NET Core Web API. Provides direct SQL access to the backend database. |
| `orchestrator` | `orchestrator:latest` | `8005:8005` | FastAPI/React Orchestrator. Manages data ingestion pipelines, dynamic proxies, and ETL. |

## Detailed Configuration

### 1. Frontend (`p2cfrontend`)
- **Build Context**: `./p2cfrontend`
- **Environment File**: `.env-frontend`
- **Dependencies**: Depends on `p2cproxy` to be available.
- **Documentation**: [FRONTEND_COMPONENTS.md](./FRONTEND_COMPONENTS.md)

### 2. Proxy (`p2cproxy`)
- **Build Context**: `./p2cproxy`
- **Environment File**: `.env-proxy`
- **Key Features**:
    - Aggregates data from multiple sources.
    - Caches geocoding results from Nominatim.
    - Manages LDAP authentication.
- **Documentation**: [BACKEND_COMPONENTS.md](./BACKEND_COMPONENTS.md#p2cproxy-nodejs)

### 3. API (`p2capi`)
- **Build Context**: `./ScalableMssqlApi`
- **Environment File**: `.env-db`
- **Role**: Raw SQL interface for the legacy database.
- **Documentation**: [BACKEND_COMPONENTS.md](./BACKEND_COMPONENTS.md#p2capi-scalablemssqlapi---net)

### 4. Orchestrator (`orchestrator`)
- **Build Context**: `./P2CScripts`
- **Environment File**: `.env-scripts`
- **Volumes**:
    - `orchestrator_db:/app/data`: Persists the local SQLite database to track Job Execution History and cached HTTP Proxies.
- **Role**:
    - Scrapes Dubuque Daily Bulletin, Sex Offender, and Jail registries using dynamic proxy pooling.
    - Automates Python ETL post-processing for infinite ingestion queue management.
    - Exposes a 'Big-Tech Light Theme' React Dashboard for real-time log monitoring and pipeline execution.
- **Documentation**: [P2C_ORCHESTRATOR.md](../P2CScripts/docs/P2C_ORCHESTRATOR.md)
