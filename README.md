<!-- ===== Task 3 Header Showcase ===== -->

<p align="center">
  <img src="https://img.shields.io/badge/Task-3-blueviolet?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Python-3.10-yellow?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Message_Broker-RabbitMQ-orange?style=for-the-badge&logo=rabbitmq" />
  <img src="https://img.shields.io/badge/Time_Series-Prophet-red?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Visualization-Matplotlib-0A66C2?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker" />
</p>

<p align="center">
  <strong>
    📈 Task 3 – Cloud Data Visualization & PM2.5 Forecasting<br/>
    🔁 RabbitMQ Consumer · 📊 Trend Plots · 🤖 15-Day ML Prediction
  </strong>
</p>

<hr/>



<h2>📈 Task 3 — Cloud Data Visualization and Forecasting (RabbitMQ → ML Model)</h2>

<p>
Task 3 focuses on building a <strong>data visualization and forecasting operator</strong> that runs on the Cloud VM.
It receives the daily-averaged PM2.5 data produced in Task 2, visualizes the historical trend, and uses a machine learning model (Prophet) to forecast PM2.5 levels for the next 15 days.
</p>

<h3>📘 Task Overview</h3>

<p>
This task connects to RabbitMQ, consumes processed air-quality data, visualizes daily averages using Matplotlib, and generates future forecasts using the Prophet time-series model. 
Both the historical and predicted plots are saved for further analysis and reporting.
</p>

<h3>✅ Implementation Summary</h3>

<ul>
  <li>The operator connects to RabbitMQ and listens to the queue:</li>
</ul>

<pre><code>pm25_daily_avg
</code></pre>

<ul>
  <li>Each incoming message contains a daily average PM2.5 value and its corresponding date.</li>
  <li>The script appends these values to in-memory lists to support plotting and forecasting.</li>
  <li>Matplotlib is used to generate a <strong>daily PM2.5 trend graph</strong>, showing variations over time.</li>
  <li>The Prophet model is applied to the dataset to forecast the next <strong>15 days</strong> of PM2.5 levels.</li>
  <li>Both plots — the daily trend and future forecast — are saved as image files for documentation.</li>
  <li>A Docker container runs the prediction service continuously on the Cloud VM.</li>
</ul>

<h3>📊 Example Data Received from RabbitMQ</h3>

<pre><code>{
  "date": "2023-10-12",
  "daily_avg": 16.73
}
</code></pre>

<h3>📈 Output Visualizations</h3>

<ul>
  <li><strong>Daily Average PM2.5 Plot:</strong> Shows trends and fluctuations over time.</li>
  <li><strong>15-Day Forecast Plot:</strong> Displays predicted PM2.5 values using Prophet.</li>
</ul>

<p>
You can insert your actual graph images here in the README for better presentation.
</p>

<h3>🚀 How to Run the Prediction Operator</h3>

<p><strong>1️⃣ Ensure RabbitMQ is running (from Task 2).</strong></p>

<p><strong>2️⃣ Run the Prediction Script</strong></p>
<pre><code>python3 predictor.py
</code></pre>

<p><strong>3️⃣ (Optional) Build and Run as a Docker Container</strong></p>
<pre><code>docker build -t pm25-predictor .
docker run --network host pm25-predictor
</code></pre>

<h3>🐳 Dockerfile Summary</h3>

<ul>
  <li>Installs dependencies including <code>matplotlib</code> and <code>prophet</code>.</li>
  <li>Copies <code>predictor.py</code> into the container.</li>
  <li>Runs the prediction script on container startup.</li>
</ul>

<h3>🎯 Outcome</h3>

<p>
Task 3 successfully visualizes historical air-quality patterns and generates a 15-day forecast using an ML model.
This prediction capability is important for understanding pollution trends and supports the edge classification process in Task 4.
</p>
