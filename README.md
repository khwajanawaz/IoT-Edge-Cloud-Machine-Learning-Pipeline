<!-- ===== Task 4 Header Showcase ===== -->

<p align="center">
  <img src="https://img.shields.io/badge/Task-4-darkgreen?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Python-3.10-yellow?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Edge_AI-TensorFlow_Lite-orange?style=for-the-badge&logo=tensorflow" />
  <img src="https://img.shields.io/badge/Classification-PM2.5-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Visualization-Matplotlib-0A66C2?style=for-the-badge" />
</p>

<p align="center">
  <strong>
    🤖 Task 4 – Edge PM2.5 Air Quality Classification (TensorFlow Lite)<br/>
    🛰️ Edge Inference · 🟢🟡🔴 AQI Classes · 📊 Visual Analytics
  </strong>
</p>

<hr/>

<h2>🤖 Task 4 — Edge Classification Using TensorFlow Lite</h2>

<p>
Task 4 focuses on deploying a <strong>lightweight classification model</strong> on the Edge VM to classify PM2.5 values into air-quality categories. 
The model is converted to <strong>TensorFlow Lite</strong> and used for <strong>on-device inference</strong>, making it suitable for edge computing scenarios with limited resources.
</p>

<h3>📘 Task Overview</h3>

<p>
The goal of this task is to take the processed PM2.5 data and classify each reading into discrete air-quality categories, such as:
</p>

<ul>
  <li><strong>Green</strong> – Good air quality</li>
  <li><strong>Yellow</strong> – Moderate air quality</li>
  <li><strong>Red</strong> – Poor air quality</li>
</ul>

<p>
The classification is performed using a TensorFlow model that has been trained offline and then converted into a <code>.tflite</code> model for edge deployment. 
The predictions are visualized using several plots to show class distribution and temporal behaviour.
</p>

<h3>📁 Directory Structure</h3>

<pre><code>.
├── task4_edge/
│   ├── task4_edge.py
│   └── task4_output/
│       ├── class_counts.png
│       ├── time_series.png
│       └── value_distribution.png
└── task4_models/
    └── models/
        ├── label_map.json
        ├── model_sizes.png
        ├── pm25_classifier.h5
        └── pm25_classifier.tflite
</code></pre>

<h3>✅ Implementation Summary</h3>

<ul>
  <li>A PM2.5 classification model is first trained and saved as a Keras model:
    <ul>
      <li><code>pm25_classifier.h5</code> – original TensorFlow/Keras model.</li>
    </ul>
  </li>
  <li>The trained model is converted into a <strong>TensorFlow Lite</strong> format:
    <ul>
      <li><code>pm25_classifier.tflite</code> – lightweight model optimized for edge inference.</li>
      <li><code>model_sizes.png</code> – comparison of model sizes before and after conversion.</li>
    </ul>
  </li>
  <li>A <code>label_map.json</code> file defines the mapping between numeric class IDs and human-readable labels (e.g. Green, Yellow, Red).</li>
  <li>The <code>task4_edge.py</code> script:
    <ul>
      <li>Loads the <code>.tflite</code> model using the TensorFlow Lite interpreter.</li>
      <li>Loads or receives PM2.5 readings (e.g., from preprocessed data or live stream).</li>
      <li>Performs inference on each PM2.5 value and assigns a class label.</li>
      <li>Aggregates predictions to generate summary statistics and visualizations.</li>
    </ul>
  </li>
</ul>

<h3>📥 Example Input for Classification</h3>

<p>
Each PM2.5 reading is treated as an input sample to the classifier, for example:
</p>

<pre><code>{
  "timestamp": "2023-10-12T10:15:00",
  "pm25_value": 22.5
}
</code></pre>

<p>
The model outputs a class ID (e.g., 0, 1, 2), which is then mapped to a label using <code>label_map.json</code>:
</p>

<pre><code>{
  "0": "Green",
  "1": "Yellow",
  "2": "Red"
}
</code></pre>

<h3>📊 Output Visualizations</h3>

<p>
The script generates several plots stored in the <code>task4_output/</code> directory:
</p>

<ul>
  <li><code>class_counts.png</code> – Bar chart showing how many readings fall into each class (Green / Yellow / Red).</li>
  <li><code>time_series.png</code> – Time-series plot of PM2.5 measurements with color-coded class labels over time.</li>
  <li><code>value_distribution.png</code> – Histogram showing the distribution of PM2.5 values and how they relate to class boundaries.</li>
</ul>

<p>
These visualizations help to understand both the numeric distribution of PM2.5 and the qualitative classification results.
</p>

<h3>🚀 How to Run the Edge Classifier</h3>

<p><strong>1️⃣ Ensure the model files are available</strong></p>

<pre><code>task4_models/models/pm25_classifier.tflite
task4_models/models/label_map.json
</code></pre>

<p><strong>2️⃣ Run the Task 4 Edge script</strong></p>

<pre><code>python3 task4_edge/task4_edge.py
</code></pre>

<p>
The script will load the TensorFlow Lite model, classify the available PM2.5 readings, and generate plots inside <code>task4_edge/task4_output/</code>.
</p>

<h3>🐳 Optional: Containerization</h3>

<p>
If desired, this edge classifier can also be packaged into a Docker container so that the same edge logic can run consistently across different environments.
</p>

<h3>🎯 Outcome</h3>

<p>
Task 4 demonstrates how a <strong>TensorFlow Lite classification model</strong> can be deployed on an Edge VM to perform real-time air-quality assessment. 
By classifying PM2.5 readings into Green, Yellow, and Red categories and providing clear visual analytics, this task completes the IoT pipeline by enabling <strong>actionable insights directly at the edge</strong>.
</p>
