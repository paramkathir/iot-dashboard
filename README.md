# IoT Sensor Dashboard

A real-time IoT monitoring dashboard built with FastAPI and Chart.js.

## Features
- Live temperature and humidity charts with smooth updates every 2 seconds
- Per-device data — switch between sensors to see individual readings
- Timeframe selector — view data across 1 hour, 1 day, 1 week, or 1 month
- Hover tooltips on charts showing time-appropriate labels per timeframe
- Alert system — sidebar warning when readings exceed safe thresholds
- Offline device handling — garage sensor shows dimmed historical data only

## Stack
- **Backend:** Python, FastAPI, Uvicorn
- **Frontend:** HTML, CSS, Chart.js
- **Data:** Simulated sensor data (compatible with real ESP32/MQTT input)

## Run Locally

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

Then open `http://localhost:8000`

## Connecting a Real Sensor
The simulated data generator in `main.py` can be swapped out for a real MQTT subscriber using `paho-mqtt`. Any ESP32 publishing temperature/humidity to an MQTT broker will work as a drop-in replacement.