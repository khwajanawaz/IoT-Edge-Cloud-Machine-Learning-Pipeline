#!/usr/bin/env python3
import os
import json
import time
import requests
import paho.mqtt.client as mqtt

BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC = os.getenv("MQTT_TOPIC", "uo/pm25")
URL = "https://raw.githubusercontent.com/ncl-iot-team/CSC8112/main/data/uo_data.min.json"
SLEEP_BETWEEN_CYCLES = int(os.getenv("SLEEP_BETWEEN_CYCLES", "60"))  # 60 s default

def fetch_pm25_data():
    resp = requests.get(URL, timeout=180)
    if resp.status_code != 200:
        print(f"❌ HTTP {resp.status_code}")
        return []
    try:
        root = json.loads(resp.content.decode("utf-8", errors="ignore"))
    except Exception as e:
        print("❌ JSON parse failed:", e)
        return []

    sensors = root.get("sensors", [])
    pm25_points = []
    for sensor in sensors:
        data_block = sensor.get("data", {})
        if not isinstance(data_block, dict):
            continue
        for readings in data_block.values():
            if not isinstance(readings, list):
                continue
            for row in readings:
                if not isinstance(row, dict):
                    continue
                if "PM2.5" not in str(row.get("Variable", "")).upper().replace(" ", ""):
                    continue
                try:
                    ts_ms = int(row["Timestamp"])
                    val = float(row["Value"])
                    ts_s = ts_ms // 1000
                    pm25_points.append({"ts": ts_s, "value": val})
                except Exception:
                    continue
    print(f" Extracted {len(pm25_points)} PM2.5 readings")
    return pm25_points

def main():
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)
    print(f"Connected to MQTT broker at {BROKER}:{PORT}")

    while True:
        pm25_points = fetch_pm25_data()
        if not pm25_points:
            print(" No data found, retrying later ...")
            time.sleep(SLEEP_BETWEEN_CYCLES)
            continue

        print(f" Publishing {len(pm25_points)} messages to '{TOPIC}' ...")
        for p in pm25_points:
            client.publish(TOPIC, json.dumps(p))
            time.sleep(0.005)
        print(f" One cycle done. Sleeping {SLEEP_BETWEEN_CYCLES} s ...\n")
        time.sleep(SLEEP_BETWEEN_CYCLES)

if __name__ == "__main__":
    main()

