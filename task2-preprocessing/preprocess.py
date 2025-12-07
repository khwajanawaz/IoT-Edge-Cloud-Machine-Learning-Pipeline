import paho.mqtt.client as mqtt
import pika, json, time, pandas as pd
from datetime import datetime

# ----------------------------- CONFIG -----------------------------
MQTT_BROKER = "localhost"          # EMQX broker (Edge)
MQTT_TOPIC = "uo/pm25"             # Topic used by Task 1 injector
RABBIT_HOST = "192.168.0.100"      # Cloud VM IP (RabbitMQ host)
QUEUE_NAME = "pm25_daily_avg"      # Queue for Task 3
OUTLIER_THRESHOLD = 50             # Values >50 are outliers
WAIT_TIME = 80                     # Seconds to collect MQTT data

# ----------------------------- CONNECT RABBITMQ -----------------------------
print(f" Connecting to RabbitMQ at {RABBIT_HOST} ...")
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME, durable=True)

# ----------------------------- COLLECT MQTT DATA -----------------------------
messages = []

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode("utf-8"))
        if "value" in data and "ts" in data:
            messages.append(data)
            if len(messages) % 500 == 0:
                print(f"📥 Received {len(messages)} messages so far ...")
    except Exception as e:
        print("⚠️ MQTT message decode error:", e)

print(f" Listening to MQTT topic '{MQTT_TOPIC}' on {MQTT_BROKER} ...")
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, 1883, 60)
client.subscribe(MQTT_TOPIC)
client.loop_start()

start_time = time.time()
while time.time() - start_time < WAIT_TIME:
    time.sleep(1)
    remaining = int(WAIT_TIME - (time.time() - start_time))
    if remaining % 5 == 0:
        print(f" {remaining}s left ... (received {len(messages)} messages so far)")

client.loop_stop()

print(f" Collected {len(messages)} raw PM2.5 readings.\n")
if len(messages) == 0:
    print(" No data received from MQTT broker!")
    connection.close()
    exit(1)

# ----------------------------- DATA CLEANING -----------------------------
df = pd.DataFrame(messages)
df["datetime"] = pd.to_datetime(df["ts"], unit="s")
df["date"] = df["datetime"].dt.date

outliers = df[df["value"] > OUTLIER_THRESHOLD]
print(f" Outliers (values > {OUTLIER_THRESHOLD}):")
print(outliers)

df_cleaned = df[df["value"] <= OUTLIER_THRESHOLD]

# ----------------------------- DAILY AVERAGING -----------------------------
daily_averages = df_cleaned.groupby("date")["value"].mean().reset_index()
print(" Daily averages computed:")
print(daily_averages.head())

# ----------------------------- SEND TO RABBITMQ -----------------------------
print(f" Sending {len(daily_averages)} daily averages to RabbitMQ queue '{QUEUE_NAME}' ...")
for _, row in daily_averages.iterrows():
    message = {
        "ts": int(datetime.strptime(str(row["date"]), "%Y-%m-%d").timestamp()),
        "avg": row["value"]
    }
    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)
    )

connection.close()
print(f" Sent {len(daily_averages)} daily averages to RabbitMQ queue '{QUEUE_NAME}'")
print(" Task 2 complete.")

