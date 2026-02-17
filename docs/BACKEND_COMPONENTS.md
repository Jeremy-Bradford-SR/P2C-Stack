# Backend Components Documentation

This document describes the backend services that support the `p2cfrontend` application.

## `p2cproxy` (Node.js)

The proxy server acts as an intermediary between the frontend and the raw SQL API, providing caching, geocoding, and data aggregation.

### Key Features
- **Data Aggregation**: The `/incidents` endpoint fetches data from multiple tables (`cadHandler`, `DailyBulletinArrests`) and combines them into a single response.
- **Geocoding**:
  - Uses `Nominatim` (OpenStreetMap) to convert addresses to coordinates.
  - Implements an in-memory cache (`node-cache`) to store geocoding results for 24 hours, reducing external API calls.
  - Enriching: Automatically attaches cached coordinates to records that lack them.
- **Proximity Search**:
  - The `/proximity` endpoint performs geospatial queries.
  - Converts WGS84 coordinates (lat/lon) to Iowa State Plane North (EPSG:2235) using `proj4` to perform accurate distance calculations in feet.
- **API Proxying**: Forwards requests to the `.NET` backend (`p2capi`) with an injected `X-API-KEY`.
- **Security**: Functionality includes `helmet` headers and rate limiting, though **authentication is currently disabled**.

### Key Endpoints
- `GET /incidents`: Main data feed (Proxy -> API).
- `GET /proximity`: Geospatial search (Proxy -> API).
- `GET /geocode`: Cached access to Nominatim.
- `GET /tables`, `/schema`: Metadata forwarding.
- `POST /login`: LDAP/Fallback authentication (JWT issuance).
- `GET /rawQuery`: **DEPRECATED** (Returns 410).

### Configuration
- `NOMINATIM_URL`: URL of the Nominatim geocoding service.
- `P2C_API_BASE`: Base URL of the `p2capi` service (e.g., `http://localhost:8083/api/Data`).
- `LDAP_*`: Configuration for Active Directory authentication.
- `JWT_SECRET`: Secret for signing tokens.

## `p2capi` (ScalableMssqlApi - .NET)

A lightweight .NET Web API that provides direct access to the SQL Server database.

### Key Features
- **Raw SQL Execution**: Allows executing arbitrary SELECT queries via the `/api/data/query` and `/api/data/rawQuery` endpoints.
- **Schema Inspection**: Provides metadata about database tables and columns.
- **Data Type Handling**: Automatically skips unsupported binary types (like `geometry` or `image`) to ensure JSON compatibility.

### Documentation
For detailed API documentation, see [ScalableMssqlApi/API_DOCUMENTATION.md](../ScalableMssqlApi/API_DOCUMENTATION.md).

## `orchestrator` (P2CScripts)

The centralized management system for data ingestion.

### Key Features
- **Job Scheduling**: Manages execution of Python scraper scripts (found in `scripts/ingestion/`).
- **Proxy Management**: 
  - Maintains a pool of valid proxies.
  - Rotates proxies to avoid IP bans during scraping.
- **Reliability**: Implements infinite retry logic for robust data collection.

### Documentation
For detailed architecture and API usage, see [P2CScripts/docs/P2C_ORCHESTRATOR.md](../P2CScripts/docs/P2C_ORCHESTRATOR.md).
