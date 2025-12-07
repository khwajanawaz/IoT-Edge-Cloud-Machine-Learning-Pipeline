import pika, json, pandas as pd, matplotlib.pyplot as plt
from datetime import datetime
import os, time, sys

# Add ML engine path
sys.path.append("/app/CSC8112_MLEngine")
from ml_engine import MLPredictor

# ---------------- CONFIG ----------------
RABBIT_HOST = "localhost"
QUEUE_NAME = "pm25_daily_avg"
OUTPUT_DIR = "/home/student/predictor_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------- CONNECT TO RABBITMQ ----------------
print(f"✅ Connecting to RabbitMQ at {RABBIT_HOST} ...")
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME, durable=True)
print(f"✅ Connected. Queue '{QUEUE_NAME}' ready.")

# ---------------- FETCH MESSAGES ----------------
messages = []
print("📩 Reading all PM2.5 daily averages from RabbitMQ ...")
deadline = time.time() + 25
while time.time() < deadline:
    method, props, body = channel.basic_get(queue=QUEUE_NAME, auto_ack=True)
    if body:
        msg = json.loads(body)
        messages.append(msg)
    else:
        time.sleep(0.2)
connection.close()

print(f"✅ Collected {len(messages)} records from queue '{QUEUE_NAME}'\n")
if not messages:
    print("⚠️ No data found. Make sure Task 2 has sent daily averages.")
    exit(0)

# ---------------- CONVERT TO DATAFRAME ----------------
df = pd.DataFrame(messages)
df["datetime"] = df["ts"].apply(lambda t: datetime.utcfromtimestamp(t))
df = df.sort_values("datetime")
print("📅 Reformatted timestamps and data preview:")
print(df.head())

# ✅ Rename columns for MLPredictor (Prophet expects Timestamp + Value)
df_ml = df.rename(columns={"datetime": "Timestamp", "avg": "Value"})

# ---------------- VISUALIZE DAILY AVERAGES ----------------
plt.figure(figsize=(10, 5))
plt.plot(df_ml['Timestamp'], df_ml['Value'], label='Daily Average PM2.5')
plt.xlabel("Date")
plt.ylabel("PM2.5 Value")
plt.title("Daily Average PM2.5 Levels")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("daily_avg.png")
plt.savefig(os.path.join(OUTPUT_DIR, "daily_avg.png"))
print(f"📊 Saved chart: {os.path.join(OUTPUT_DIR, 'daily_avg.png')}")

# ------------------ Run ML Predictor -------------------
print("🤖 Running ML Engine to predict next 15 days ...")
ml_engine = MLPredictor(df_ml)
ml_engine.train()
forecast = ml_engine.predict()
fig = ml_engine.plot_result(forecast)
fig.savefig(os.path.join(OUTPUT_DIR, "forecast.png"))
print(f"📈 Saved forecast: {os.path.join(OUTPUT_DIR, 'forecast.png')}")
print("🏁 Task 3 complete.")
