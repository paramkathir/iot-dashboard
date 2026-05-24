import random
import time
import math
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import threading

app = FastAPI()

DEVICES = [
    {"id": "living_room", "name": "Living Room", "status": "online"},
    {"id": "bedroom",     "name": "Bedroom",     "status": "online"},
    {"id": "garage",      "name": "Garage",       "status": "offline"},
]

def generate_history(hours, interval_seconds, base_temp, base_hum):
    now = time.time()
    points = int((hours * 3600) / interval_seconds)
    temps, hums, timestamps = [], [], []
    t = base_temp
    h = base_hum
    for i in range(points):
        t += random.uniform(-0.3, 0.3)
        t = max(15.0, min(35.0, t))
        h += random.uniform(-0.5, 0.5)
        h = max(30.0, min(80.0, h))
        ts = now - (points - i) * interval_seconds
        temps.append(round(t, 1))
        hums.append(round(h, 1))
        timestamps.append(ts)
    return temps, hums, timestamps

device_store = {
    "living_room": {
        "base_temp": 22.0, "base_hum": 55.0,
        "temperature": [], "humidity": [], "timestamps": []
    },
    "bedroom": {
        "base_temp": 20.0, "base_hum": 60.0,
        "temperature": [], "humidity": [], "timestamps": []
    },
    "garage": {
        "base_temp": 18.0, "base_hum": 45.0,
        "temperature": [], "humidity": [], "timestamps": []
    },
}

# Pre-fill one month of data
for dev_id, dev in device_store.items():
    temps, hums, tss = generate_history(24 * 30, 900, dev["base_temp"], dev["base_hum"])
    dev["temperature"] = temps
    dev["humidity"]    = hums
    dev["timestamps"]  = tss

OFFLINE_DEVICES = {"garage"}

def simulate_sensors():
    while True:
        now = time.time()
        for dev_id, dev in device_store.items():
            if dev_id in OFFLINE_DEVICES:
                continue
            t = dev["temperature"][-1] if dev["temperature"] else dev["base_temp"]
            h = dev["humidity"][-1]    if dev["humidity"]    else dev["base_hum"]
            t += random.uniform(-0.3, 0.3)
            t = max(15.0, min(35.0, t))
            h += random.uniform(-0.5, 0.5)
            h = max(30.0, min(80.0, h))
            dev["temperature"].append(round(t, 1))
            dev["humidity"].append(round(h, 1))
            dev["timestamps"].append(now)
        time.sleep(2)

thread = threading.Thread(target=simulate_sensors, daemon=True)
thread.start()

TIMEFRAME_HOURS = {"1h": 1, "1d": 24, "1w": 168, "1m": 720}
MAX_POINTS      = {"1h": 60, "1d": 48, "1w": 56, "1m": 60}

@app.get("/data")
def get_data(device: str = "living_room", timeframe: str = "1h"):
    dev  = device_store.get(device, device_store["living_room"])
    hrs  = TIMEFRAME_HOURS.get(timeframe, 1)
    maxp = MAX_POINTS.get(timeframe, 60)
    cutoff = time.time() - hrs * 3600

    temps, hums, tss = [], [], []
    for t, h, ts in zip(dev["temperature"], dev["humidity"], dev["timestamps"]):
        if ts >= cutoff:
            temps.append(t)
            hums.append(h)
            tss.append(ts)

    step = max(1, len(temps) // maxp)
    temps = temps[::step]
    hums  = hums[::step]
    tss   = tss[::step]

    status = next(d["status"] for d in DEVICES if d["id"] == device)
    latest_temp = temps[-1] if temps else 0
    latest_hum  = hums[-1]  if hums  else 0
    alert = latest_temp > 30 or latest_temp < 17 or latest_hum > 75 or latest_hum < 35

    return {
        "temperature": temps,
        "humidity":    hums,
        "timestamps":  tss,
        "latest_temp": latest_temp,
        "latest_hum":  latest_hum,
        "status":      status,
        "alert":       alert,
        "timeframe":   timeframe,
        "devices":     DEVICES,
    }

@app.get("/", response_class=HTMLResponse)
def dashboard():
    with open("index.html", encoding="utf-8") as f:
        return f.read()