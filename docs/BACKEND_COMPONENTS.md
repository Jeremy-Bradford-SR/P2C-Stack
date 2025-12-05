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
- **API Proxying**: Forwards requests for tables, schema, and raw queries to the `p2capi`.

### Key Endpoints
- `GET /incidents`: Main data feed for the dashboard. Supports filtering by date, limit, and distance.
- `GET /proximity`: Search for incidents within a radius of an address.
- `GET /geocode`: Direct access to the geocoding service.
- `GET /tables`, `/schema`, `/query`: Proxies to `p2capi`.

### Configuration
- `NOMINATIM_URL`: URL of the Nominatim geocoding service.
- `P2C_API_BASE`: Base URL of the `p2capi` service.

## `p2capi` (ScalableMssqlApi - .NET)

A lightweight .NET Web API that provides direct access to the SQL Server database.

### Key Features
- **Raw SQL Execution**: Allows executing arbitrary SELECT queries via the `/api/data/query` and `/api/data/rawQuery` endpoints.
- **Schema Inspection**: Provides metadata about database tables and columns.
- **Data Type Handling**: Automatically skips unsupported binary types (like `geometry` or `image`) to ensure JSON compatibility.

### Documentation
For detailed API documentation, see [ScalableMssqlApi/API_DOCUMENTATION.md](../ScalableMssqlApi/API_DOCUMENTATION.md).
