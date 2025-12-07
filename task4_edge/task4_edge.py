#!/usr/bin/env python3
"""
Task 4 – Edge Inference Script

(a) Load TensorFlow Lite model
(b) Subscribe to MQTT broker
(c) Collect/batch JSON data from MQTT
(d) Classify each PM2.5 reading as Green/Yellow/Red
(e) Log results to console
(f) Visualize:
    - bar-chart of class counts
    - time-series plot with color-coded points
    - PM2.5 value distribution
"""

import os
import json
import time
from datetime import datetime

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")   # no GUI on server
import matplotlib.pyplot as plt

import paho.mqtt.client as mqtt
import tensorflow as tf   # ✅ use tf.lite.Interpreter

# ---------------- CONFIG ----------------
# MQTT broker (your EMQX on Edge)
MQTT_HOST = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "uo/pm25"   # same topic used in Task 1

# Paths to model + label map (copied from Cloud to Edge)
# 🔴 If your files are directly in task4_models/, change MODEL_DIR accordingly.
MODEL_DIR = "/home/student/IOT-coursework/task4_models/models"
TFLITE_MODEL_PATH = os.path.join(MODEL_DIR, "pm25_classifier.tflite")
LABEL_MAP_PATH = os.path.join(MODEL_DIR, "label_map.json")

# Where to save plots
OUT_DIR = "/home/student/IOT-coursework/task4_edge/task4_output"
os.makedirs(OUT_DIR, exist_ok=True)

# How long to listen to MQTT (seconds)
RUN_SECONDS = 60

# ---------------- LOAD LABEL MAP ----------------
with open(LABEL_MAP_PATH, "r") as f:
    raw_label_map = json.load(f)

# raw_label_map is like {"0": "GREEN", "1": "RED", "2": "YELLOW"}
index_label_pairs = sorted(
    ((int(k), v) for k, v in raw_label_map.items()),
    key=lambda x: x[0]
)
class_names = [v for (_, v) in index_label_pairs]
print("🏷️ Class names (index → label):")
for idx, name in enumerate(class_names):
    print(f"  {idx} → {name}")

# ---------------- LOAD TFLITE MODEL ----------------
print(f"\n📦 Loading TFLite model from {TFLITE_MODEL_PATH} ...")
interpreter = tf.lite.Interpreter(model_path=TFLITE_MODEL_PATH)  # ✅ use tf.lite.Interpreter
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("✅ TFLite model loaded and ready.\n")

# ---------------- MQTT + INFERENCE ----------------
results = []  # will collect dicts of {ts, value, label}

def classify_pm25(value: float) -> str:
    """
    Run the TFLite model on a single PM2.5 value and return class label.
    Model was trained on raw 'Value' (no scaling), so we pass it directly.
    """
    x = np.array([[value]], dtype=np.float32)
    interpreter.set_tensor(input_details[0]["index"], x)
    interpreter.invoke()
    probs = interpreter.get_tensor(output_details[0]["index"])[0]
    class_id = int(np.argmax(probs))
    return class_names[class_id]

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)

        pm_value = float(data.get("value", 0.0))
        ts = int(data.get("ts", time.time()))

        label = classify_pm25(pm_value)

        results.append({
            "ts": ts,
            "value": pm_value,
            "label": label,
        })

        dt_str = datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        print(f"📩 [{dt_str}] PM2.5={pm_value:.2f} → {label}")

    except Exception as e:
        print("⚠️ Error processing MQTT message:", e)

# ---------------- MAIN COLLECTION LOOP ----------------
print(f"✅ Connecting to MQTT at {MQTT_HOST}:{MQTT_PORT} ...")
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_HOST, MQTT_PORT, 60)
client.subscribe(MQTT_TOPIC)
client.loop_start()

print(f"⏳ Collecting PM2.5 readings for {RUN_SECONDS} seconds ...")
time.sleep(RUN_SECONDS)

client.loop_stop()
client.disconnect()

print(f"\n✅ Done listening. Collected {len(results)} classified readings.\n")

if not results:
    print("⚠️ No data collected from MQTT. Make sure injector is running and publishing on 'uo/pm25'.")
    exit(0)

# ---------------- CONVERT TO DATAFRAME ----------------
df = pd.DataFrame(results)
df["datetime"] = df["ts"].apply(lambda t: datetime.utcfromtimestamp(t))

print("📋 Sample of classified data:")
print(df.head())

# ---------------- VISUALIZATION (a): BAR CHART ----------------
counts = df["label"].value_counts().reindex(class_names, fill_value=0)
plt.figure(figsize=(6, 4))
counts.plot(kind="bar")
plt.title("PM2.5 Classification Counts")
plt.xlabel("Class")
plt.ylabel("Count")
plt.tight_layout()
bar_path = os.path.join(OUT_DIR, "class_counts.png")
plt.savefig(bar_path)
print(f"📊 Saved class count bar chart → {bar_path}")

# ---------------- VISUALIZATION (b): TIME-SERIES ----------------
plt.figure(figsize=(10, 5))
for label in class_names:
    sub = df[df["label"] == label]
    if sub.empty:
        continue
    plt.scatter(sub["datetime"], sub["value"], label=label, s=10)
plt.title("PM2.5 Time-series with Classifications")
plt.xlabel("Time")
plt.ylabel("PM2.5 Value")
plt.grid(True)
plt.legend()
plt.tight_layout()
ts_path = os.path.join(OUT_DIR, "time_series.png")
plt.savefig(ts_path)
print(f"📈 Saved time-series plot → {ts_path}")

# ---------------- VISUALIZATION (c): VALUE DISTRIBUTION ----------------
plt.figure(figsize=(6, 4))
plt.hist(df["value"], bins=30)
plt.title("PM2.5 Value Distribution")
plt.xlabel("PM2.5")
plt.ylabel("Frequency")
plt.tight_layout()
dist_path = os.path.join(OUT_DIR, "value_distribution.png")
plt.savefig(dist_path)
print(f"📉 Saved distribution plot → {dist_path}")

# ---------------- SUMMARY ----------------
print("\n📊 Classification summary (counts):")
print(counts)

print(f"\n📁 All figures saved in: {OUT_DIR}")
print("🎉 Task 4 (5a–5f) edge classification + visualization complete.")

