# P2C Frontend Performance Evaluation

## Overview
`p2cfrontend` is a Single Page Application (SPA) built with React and Vite. It serves as the primary dashboard for viewing complex public safety data.

## Key Findings

### 1. Initial Load & Data Fetching
- **Strategy**: **Eager Loading**. The application fetches *all* datasets (Incidents, Traffic, Jail, Sex Offenders, etc.) in parallel upon initial load (`App.jsx` -> `fetchData`).
- **Impact**: 
    - **Pros**: Immediate interactivity when switching tabs once loaded.
    - **Cons**: High initial network bandwidth and latency. If datasets grow large (e.g., historical replay), startup time will degrade significantly.
- **Optimization Potential**: Lazy load tab-specific data when the user navigates to that tab.

### 2. Rendering & State Management
- **Memoization**: Good use of `useMemo` in `DataScience.jsx` and `App.jsx` to prevent expensive recalculations of derived statistics and chart data.
- **Large Lists**: 
    - `DataGrid` renders rows directly. For datasets > 500 rows, this may cause UI lag.
    - **Recommendation**: Implement windowing/virtualization (e.g., `react-window`) for data grids.
- **Tab Switching**: 
    - **Behavior**: `Tabs.jsx` conditionally renders only the active tab. Inactive tabs are **unmounted** from the DOM.
    - **Impact**: 
        - **Pros**: Low memory usage when idling on a simple tab.
        - **Cons**: High CPU cost when switching tabs, as heavy components (Maps, Charts) must fully re-mount and re-calculate layout.

### 3. Maps (`MapView`)
- **Clustering**: Correctly uses `react-leaflet-cluster` to manage visual clutter.
- **Marker Overhead**: The component maps *all* data points to `Marker` React elements before passing them to the cluster group. For thousands of points, this instantiation tax is heavy.
- **Images**: In-line Base64 images in `photo_data` bloat the JavaScript heap memory.

### 4. Build & Bundle
- **Tooling**: Built with Vite, ensuring fast HMR during development and optimized Rollup builds for production.
- **Dependencies**: 
    - `recharts`: Large library, but necessary for analytics.
    - `leaflet`: Standard weight.
    - No obvious unused heavy libraries found in `package.json`.

## Recommendations
1.  **Virtualize Data Grids**: Use `react-window` or `react-virtuoso` for tables to support 1000+ rows smoothly.
2.  **Lazy Data Fetching**: Move API calls from `App.jsx` into specific tab components (e.g., `fetchJailData` only when Jail tab opens).
3.  **Optimize Map Markers**: Use proper GeoJSON layers or optimized clustering that doesn't instantiate React components for every hidden point.
4.  **Pagination/Infinite Scroll**: The backend supports limits, but the frontend currently requests large fixed chunks (1000 records). Implement dynamic loading.
