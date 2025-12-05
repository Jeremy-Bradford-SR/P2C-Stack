# Frontend Components Documentation

This document describes the key React components and utilities in the `p2cfrontend` application.

## Core Components

### `App.jsx`
The main application container.
- **Responsibilities**:
  - Fetches initial data from all API endpoints (Incidents, Traffic, Violators, Sex Offenders, Probation/Parole, Dispatch, Jail).
  - Manages global state (data results, loading state, map points).
  - Handles background geocoding of addresses.
  - Renders the main `Tabs` navigation and the content for each tab.
  - Manages modals for Jail Inmates and Sex Offenders.

### `DataScience.jsx`
A comprehensive analytics dashboard.
- **Features**:
  - **Overview**: Aggregate stats and trends across all data sources.
  - **Sub-tabs**: Dedicated analytics for CAD, Arrests, Crime, Traffic, Probation/Parole, Sex Offenders, and Jail.
  - **Visualizations**: Uses `recharts` for line, bar, pie, and area charts.
  - **Mapping**: Embeds `react-leaflet` maps for geospatial analysis (heatmaps, clusters).
  - **Interval Selection**: Allows filtering data by time range (1 week to 1 year), triggering full dataset fetches.

### `Incidents.jsx`
The view for the "Recent" tab.
- **Layout**: Uses `SplitView` to show a map on top and three data grids (CAD, Arrests, Crime) below.
- **Functionality**: Displays a subset of recent data. Clicking rows zooms the map to the location.

### `MapWithData.jsx`
A reusable component for tabs that need both a map and a list of records (e.g., Crime, Arrests, Traffic).
- **Props**: `data`, `columns`, `loading`, `mapHeight`, `setMapHeight`, `onRowClick`.
- **Structure**: Wraps `FilterableDataGrid` and `MapView` inside a `SplitView`.
- **Behavior**: Filters applied to the grid also filter the points shown on the map.

### `Proximity.jsx`
Provides a search interface for finding incidents near a specific address.
- **Inputs**: Address, Days (time range), Distance (radius), Nature (optional keyword).
- **Output**: Displays results in a `MapWithData` view.

## UI & Utility Components

### `FilterableDataGrid.jsx`
A wrapper around `DataGrid` that adds search and date filtering.
- **Components**: Renders `FilterControls` above a `DataGrid`.
- **Logic**: Filters data based on text match (across all fields) and date range checks on common date fields (`event_time`, `starttime`, etc.).

### `DataGrid.jsx`
A generic table component for displaying arrays of objects.
- **Props**: `data`, `columns`, `onRowClick`.
- **Features**:
  - Auto-resolves cell values based on keys.
  - Handles common field aliases (e.g., `event_time` vs `starttime`).
  - Formats location strings (removes "at ", handles coordinates).

### `FilterControls.jsx`
A UI component containing inputs for filtering data.
- **Inputs**: Text search, Start Date, End Date.
- **Exports**: `FilterControls` (component) and `filterData` (helper function).

### `SplitView.jsx`
A layout component that divides the screen vertically between a map and content.
- **Features**:
  - Resizable divider (drag to adjust map height).
  - Contains `MapView` in the top section and `children` in the bottom.
  - Provides "Fit All Markers" and "Center on Dubuque" buttons.

### `Tabs.jsx` / `Tab`
Simple tabbed navigation components.
- **Tabs**: Manages active tab state and renders the tab header list.
- **Tab**: A wrapper for content, identified by a `label`.

### `MapView.jsx`
A wrapper around `react-leaflet` components.
- **Features**:
  - Renders `MapContainer`, `TileLayer`, and `MarkerClusterGroup`.
  - Maps data points to `Marker`s with custom icons based on source (CAD, Arrest, Crime, etc.).
  - Displays `Popup`s with record details and photos (if available).

### `client.js`
The API client module.
- **Features**:
  - Configures `axios` with base URL and auth headers (though auth is currently disabled).
  - Exports functions for each data source (`getIncidents`, `getTraffic`, `getJailInmates`, etc.).
  - Handles `rawQuery` calls to the proxy.

## Legacy / Unused

- **`Login.jsx`**: Previous authentication component. Currently unused as auth is disabled.
- **`Offenders.jsx`**: Likely a legacy component, superseded by `FilterableDataGrid` usage in the "Violators" tab.
