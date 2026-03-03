<h2>Build With TRAE Hackathon Project</h2>

<h2>Theme: Climate Tech Optimization Engines</h2>

<h4>📌 Problem Statement</h4>

Energy waste in institutional buildings occurs due to invisible inefficiencies such as:

Air conditioners running in unoccupied rooms

Lights left on after operational hours

Peak load mismanagement

Lack of predictive demand planning

No carbon impact simulation

Most existing systems only monitor energy consumption but do not optimize it.

<h4>💡 Our Solution</h4>

EnergiAI is an AI-driven autonomous optimization engine that:

Forecasts future energy demand

Detects inefficiencies using anomaly detection

Optimizes peak load consumption

Simulates carbon reduction impact

Generates actionable AI-based recommendations

It transforms invisible energy waste into measurable climate action.

<h4>🧠 System Architecture</h4>

EnergiAI follows a layered closed-loop architecture:

Data Collection Layer

Data Processing & Feature Engineering

Forecasting Engine

Waste Detection Engine

Optimization Engine

Carbon Impact & What-If Simulator

Recommendation Engine

Visualization Dashboard

Continuous learning feedback improves future predictions.

See: architecture_diagram.png

<h4>🏗 Core Modules</h4>
<h5>🔹 1. Data Processing Module</h5>

Cleans dataset

Converts timestamps

Extracts hour & peak indicators

Prepares features for AI models

<h5>🔹 2. Forecasting Engine</h5>

Predicts short-term energy demand

Identifies potential peak hours

Provides baseline consumption forecast

Technique: Time-based regression / Prophet

<h5>🔹 3. Waste Detection Engine</h5>

Uses Isolation Forest

Detects abnormal consumption spikes

Identifies standby and night waste

<h5>🔹 4. Optimization Engine</h5>

Detects top 10% peak loads

Applies configurable reduction logic

Smooths demand curve

Goal: Reduce peak load by 15–25%

<h5>🔹 5. Carbon Impact Simulator</h5>

Calculates CO₂ emissions

Compares baseline vs optimized

Estimates carbon reduction percentage

Emission factor: 0.82 kg CO₂ per kWh (configurable)

<h5>🔹 6. What-If Simulation Engine</h5>

Allows scenario simulation such as:

“What if AC runtime reduces by 20%?”

“What if peak usage shifts to off-peak hours?”

Generates:

Energy savings

Carbon reduction

Cost savings

<h5>🔹 7. Recommendation Engine</h5>

Generates AI-powered suggestions:

Reduce AC runtime during peak hours

Shift high-energy operations

Implement load smoothing

<h5>🔹 8. Visualization Layer</h5>

Streamlit dashboard showing:

Baseline vs Optimized graph

Forecast curve

Anomaly highlighting

Carbon savings metrics

KPI indicators

<h4>🛠 Tech Stack</h4>

Python

Pandas

Scikit-learn

Streamlit

Prophet (optional forecasting)
