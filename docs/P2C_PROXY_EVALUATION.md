# P2C Proxy Evaluation

## Overview
`p2cproxy` is a Node.js/Express middleware service that sits between the frontend and the backend API (`p2capi`). It primarily handles request forwarding, geocoding with caching, and basic security headers.

## Key Findings

### 1. Security & Authentication
- **Authentication State**: **DISABLED**. 
    - The `authenticateToken` middleware explicitly calls `next()` without verifying tokens.
    - Requires immediate attention if this service is exposed to the public internet.
- **Login Endpoint**: Exists (`POST /login`) and supports LDAP, but the issued JWT is currently ignored by the middleware.
- **Hardcoded Credentials**: A fallback logic exists for `admin` / `password` if LDAP is not configured.
- **Protection**: Uses `helmet` for headers and `express-rate-limit` (1000 requests / 15 mins).

### 2. Geocoding & Caching
- **Service**: Proxies requests to an internal Nominatim instance.
- **Caching**: 
    - Uses `node-cache` (in-memory).
    - **TTL**: 24 hours, which is efficient for static address data.
    - **Logic**: Checks cache before calling the external Nominatim service, significantly reducing load.

### 3. API Forwarding
- **Architecture**: Acts as a "pass-through" for most data endpoints.
    - Forwards requests to `P2C_API_BASE` (default: `http://localhost:8083/api/Data`).
    - Injects an `X-API-KEY` header for upstream security.
- **Endpoints**:
    - **Legacy**: `/incidents`, `/proximity` (now forwarded to API).
    - **Direct Proxy**: `/tables`, `/schema`, `/traffic`, `/jail`, `/dispatch`, `/stats`.
    - **Deprecated**: `/rawQuery` returns `410 Gone`.

## Recommendations
1.  **Re-enable Authentication**: If the system is production-facing, the `authenticateToken` middleware should be uncommented/fixed to verify JWTs.
2.  **Remove Hardcoded Credentials**: The fallback `admin/password` logic should be removed or strictly controlled via environment variables.
3.  **Externalize Rate Limit Store**: For a clustered deployment, `express-rate-limit`'s in-memory store won't work well; consider Redis.
4.  **Standardize Error Handling**: Uniform error responses for upstream failures (currently forwards upstream errors or returns 502).

### 5. Performance Analysis
- **Strengths**:
    - **Caching**: `node-cache` prevents redundant calls to the Nominatim service, which is the system's slowest dependency.
    - **Compression**: `compression` middleware reduces payload size for JSON responses.
- **Bottlenecks**:
    - **Single-Threaded**: The application runs as a single process (`node index.js`). It does not utilize `cluster` or a process manager (like PM2) to leverage multi-core CPUs.
    - **Synchronous Calculations**: `proj4` coordinate transformations execute on the main thread. Heavy load on `/proximity` could block the event loop.
    - **No Connection Pooling**: Upstream API requests via `axios` do not appear to use a persistent `httpAgent` with `keepAlive`. This means a new TCP handshake may occur for every forwarded request, increasing latency.
    - **Unbounded Cache**: usage of `node-cache` does not define a `maxKeys` limit. In a worst-case scenario with random/unique queries, this could lead to memory exhaustion (OOM).
