<p align="center"> <img src="https://img.shields.io/badge/IoT-Edge%20Computing-blue?style=for-the-badge&logo=iota" /> <img src="https://img.shields.io/badge/Cloud-Azure-blue?style=for-the-badge&logo=microsoftazure" /> <img src="https://img.shields.io/badge/MQTT-EMQX-brightgreen?style=for-the-badge&logo=mqtt" /> <img src="https://img.shields.io/badge/AMQP-RabbitMQ-orange?style=for-the-badge&logo=rabbitmq" /> <img src="https://img.shields.io/badge/Docker-Microservices-2496ED?style=for-the-badge&logo=docker" /> <img src="https://img.shields.io/badge/Python-3.10-yellow?style=for-the-badge&logo=python" /> <img src="https://img.shields.io/badge/ML-Prophet-red?style=for-the-badge&logo=python" /> <img src="https://img.shields.io/badge/Edge%20AI-TensorFlow%20Lite-orange?style=for-the-badge&logo=tensorflow" /> </p> <p align="center"><strong> 📡 Full Edge–Cloud IoT Machine Learning Pipeline 🌫 Real PM2.5 Sensor Data | 🤖 Prediction + Classification | 🐳 Dockerized Microservices Developed by <u>Khwaja Nawaz</u> </strong></p>

<p align="center"> <img src="https://img.shields.io/badge/Task-1-blue?style=for-the-badge" /> <img src="https://img.shields.io/badge/Python-3.10-yellow?style=for-the-badge&logo=python" /> <img src="https://img.shields.io/badge/MQTT-EMQX-brightgreen?style=for-the-badge&logo=mqtt" /> <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker" /> <img src="https://img.shields.io/badge/Data-PM2.5-red?style=for-the-badge" /> </p> <p align="center"><strong> 📡 Task 1 — Data Injector for PM2.5 IoT Sensor Streams Developed by <u>Khwaja Nawaz</u> </strong></p>

<h2>📘 Task-1 Overview</h2>

<p>
The purpose of Task 1 is to design and implement a <strong>Data Injector</strong> that collects real PM2.5 sensor readings from the Urban Observatory API and publishes them to an <strong>EMQX MQTT broker</strong>, enabling downstream tasks to access live air-quality data.
</p>

<h3>✅ Implementation Summary</h3>

<ul>
  <li>The EMQX MQTT broker image was pulled from Docker Hub and deployed on the Edge VM.</li>
  <li>A Python script (<code>injector.py</code>) was developed to fetch PM2.5 data from the Urban Observatory API.</li>
  <li>The script processes the raw dataset and extracts:
    <ul>
      <li><strong>timestamp</strong></li>
      <li><strong>value</strong> (PM2.5 concentration)</li>
    </ul>
  </li>
  <li>After extraction, all PM2.5 readings are published to the MQTT broker under the topic:
    <pre><code>uo/pm25</code></pre>
  </li>
  <li>Once executed, the injector automatically connects to <strong>localhost:1883</strong> and begins sending readings.</li>
  <li>The injector runs in a continuous loop, repeatedly publishing all PM2.5 readings until it is manually stopped.</li>
</ul>

<h3>🔗 MQTT Topic Used</h3>

<pre><code>uo/pm25
</code></pre>

<p><strong>Example Published Message:</strong></p>

<pre><code>{
  "timestamp": 1697034211,
  "value": 14.72
}
</code></pre>

<h3>🚀 How to Run the Data Injector</h3>

<p><strong>1️⃣ Start EMQX MQTT Broker</strong></p>
<pre><code>docker run -d --name emqx -p 1883:1883 emqx/emqx
</code></pre>

<p><strong>2️⃣ Run Injector Without Docker</strong></p>
<pre><code>python3 injector.py
</code></pre>

<p><strong>3️⃣ Build the Docker Image</strong></p>
<pre><code>docker build -t data-injector .
</code></pre>

<p><strong>4️⃣ Run the Injector Inside Docker</strong></p>
<pre><code>docker run --network host data-injector
</code></pre>

<h3>🐳 Dockerfile Summary</h3>

<ul>
  <li>Installs required Python dependencies.</li>
  <li>Copies the injector script into the image.</li>
  <li>Automatically executes the script when the container starts.</li>
</ul>



<p align="center"> <img src="https://img.shields.io/badge/Task-2-blue?style=for-the-badge" /> <img src="https://img.shields.io/badge/Python-3.10-yellow?style=for-the-badge&logo=python" /> <img src="https://img.shields.io/badge/MQTT-Subscriber-brightgreen?style=for-the-badge&logo=mqtt" /> <img src="https://img.shields.io/badge/AMQP-RabbitMQ-orange?style=for-the-badge&logo=rabbitmq" /> <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker" /> </p> <p align="center"><strong> 🧹 Task 2 — Data Preprocessing Operator Developed by <u>Khwaja Nawaz</u> </strong></p>

<h2>🧹 Task 2 — Data Preprocessing Operator (MQTT → RabbitMQ)</h2>

<p>
Task 2 focuses on designing a <strong>Data Preprocessing Operator</strong> that subscribes to PM2.5 data from the MQTT broker, filters and cleans the readings, computes daily averages, and forwards the processed data to a RabbitMQ queue for use in Task 3.
</p>

<h3>📘 Task-2 Overview</h3>

<p>
The operator runs as a Dockerized service on the Edge VM, consuming PM2.5 messages published by Task 1 and transforming them into a clean, structured format suitable for machine learning and forecasting.
</p>

<h3>✅ Implementation Summary</h3>

<ul>
  <li>The <code>preprocess.py</code> script subscribes to the MQTT topic:</li>
</ul>

<pre><code>uo/pm25
</code></pre>

<ul>
  <li>Incoming PM2.5 readings are collected in real time.</li>
  <li>The script filters out <strong>outliers</strong>, specifically values <strong>greater than 50</strong>.</li>
  <li>Valid readings are grouped by day (24-hour window) using their timestamps.</li>
  <li>A <strong>daily average PM2.5 value</strong> is calculated for each day.</li>
  <li>The processed results are published to RabbitMQ under the queue:</li>
</ul>

<pre><code>pm25_daily_avg
</code></pre>

<ul>
  <li>The operator runs inside a Docker container, and logs can be viewed using:
    <pre><code>docker logs preprocess</code></pre>
  </li>
  <li>The provided <code>docker-compose.yml</code> file launches both RabbitMQ and the preprocessing operator together.</li>
</ul>

<h3>🔗 Input and Output Topics/Queues</h3>

<p><strong>Input (MQTT Topic from Task 1):</strong></p>
<pre><code>uo/pm25
</code></pre>

<p><strong>Output (RabbitMQ Queue for Task 3):</strong></p>
<pre><code>pm25_daily_avg
</code></pre>

<h3>📤 Example Processed Output</h3>

<pre><code>{
  "date": "2023-10-12",
  "daily_avg": 16.73
}
</code></pre>

<h3>🚀 How to Run the Preprocessing Operator</h3>

<p><strong>1️⃣ Start RabbitMQ and Preprocessor Using Docker Compose</strong></p>
<pre><code>docker compose up -d
</code></pre>

<p><strong>2️⃣ View Logs</strong></p>
<pre><code>docker logs preprocess
</code></pre>

<p><strong>3️⃣ Run Without Docker (Testing Only)</strong></p>
<pre><code>python3 preprocess.py
</code></pre>

<h3>🐳 Dockerfile Summary</h3>

<ul>
  <li>Installs required dependencies such as <code>paho-mqtt</code> and <code>pika</code>.</li>
  <li>Copies the preprocessing script into the container.</li>
  <li>Runs the operator automatically when the container starts.</li>
</ul>

<h3>🎯 Outcome</h3>

<p>
Task 2 successfully transforms raw PM2.5 sensor readings into clean, daily averaged values. The processed data is forwarded to RabbitMQ, enabling Task 3 to perform visualization and machine learning forecasting.
</p>



