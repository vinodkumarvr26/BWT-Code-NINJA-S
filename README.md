Build With TRAE Hackathon Project

Theme: Climate Tech Optimization Engines

📌 Problem Statement

Energy waste in institutional buildings occurs due to invisible inefficiencies such as:

Air conditioners running in unoccupied rooms

Lights left on after operational hours

Peak load mismanagement

Lack of predictive demand planning

No carbon impact simulation

Most existing systems only monitor energy consumption but do not optimize it.

💡 Our Solution

EnergiAI is an AI-driven autonomous optimization engine that:

Forecasts future energy demand

Detects inefficiencies using anomaly detection

Optimizes peak load consumption

Simulates carbon reduction impact

Generates actionable AI-based recommendations

It transforms invisible energy waste into measurable climate action.

🧠 System Architecture

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

🏗 Core Modules
🔹 1. Data Processing Module

Cleans dataset

Converts timestamps

Extracts hour & peak indicators

Prepares features for AI models

🔹 2. Forecasting Engine

Predicts short-term energy demand

Identifies potential peak hours

Provides baseline consumption forecast

Technique: Time-based regression / Prophet

🔹 3. Waste Detection Engine

Uses Isolation Forest

Detects abnormal consumption spikes

Identifies standby and night waste

🔹 4. Optimization Engine

Detects top 10% peak loads

Applies configurable reduction logic

Smooths demand curve

Goal: Reduce peak load by 15–25%

🔹 5. Carbon Impact Simulator

Calculates CO₂ emissions

Compares baseline vs optimized

Estimates carbon reduction percentage

Emission factor: 0.82 kg CO₂ per kWh (configurable)

🔹 6. What-If Simulation Engine

Allows scenario simulation such as:

“What if AC runtime reduces by 20%?”

“What if peak usage shifts to off-peak hours?”

Generates:

Energy savings

Carbon reduction

Cost savings

🔹 7. Recommendation Engine

Generates AI-powered suggestions:

Reduce AC runtime during peak hours

Shift high-energy operations

Implement load smoothing

🔹 8. Visualization Layer

Streamlit dashboard showing:

Baseline vs Optimized graph

Forecast curve

Anomaly highlighting

Carbon savings metrics

KPI indicators

🛠 Tech Stack

Python

Pandas

Scikit-learn

Streamlit

Prophet (optional forecasting)
