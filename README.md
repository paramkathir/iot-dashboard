# IoT Sensor Dashboard

A real-time IoT monitoring dashboard built with FastAPI and Chart.js. The project simulates multiple environmental sensors, exposes their telemetry through a FastAPI endpoint, and visualizes current and historical readings in a browser dashboard.

## Features

- Live temperature and humidity charts with updates every 2 seconds
- Per-device views for individual sensor readings
- Timeframe selector for 1 hour, 1 day, 1 week, and 1 month
- Downsampled historical responses to keep long-range charts manageable
- Hover tooltips with timeframe-aware labels
- Threshold-based alerts for temperature and humidity
- Offline-device handling with historical data preserved for the unavailable sensor
- Pre-generated historical telemetry for longer timeframe views

## Data Flow

```mermaid
flowchart LR
    A[Sensor Simulator<br/>Python background thread] --> B[In-memory<br/>device store]
    B --> C[FastAPI<br/>/data endpoint]
    C --> D[Browser Dashboard<br/>HTML + CSS + Chart.js]
    D -->|device + timeframe| C
```

The Python backend maintains separate temperature, humidity, and timestamp histories for each simulated device. Online devices receive new readings every two seconds, while the offline device keeps its historical data without generating new samples.

When the dashboard requests `/data`, FastAPI filters readings to the selected timeframe and downsamples longer histories before returning them to the frontend. The API also calculates the latest values, device status, and whether the current reading crosses an alert threshold.

## Stack

- **Backend:** Python, FastAPI, Uvicorn
- **Frontend:** HTML, CSS, Chart.js
- **Data:** Simulated sensor telemetry stored in memory

## Run Locally

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

Then open `http://localhost:8000`.

## Connecting a Real Sensor

The current project intentionally uses simulated telemetry so the dashboard can run without external hardware. The simulator can be replaced with an MQTT subscriber, such as one built with `paho-mqtt`, while keeping the dashboard and API layer largely unchanged. An ESP32 or other edge device could then publish temperature and humidity readings to the MQTT broker for visualization.
