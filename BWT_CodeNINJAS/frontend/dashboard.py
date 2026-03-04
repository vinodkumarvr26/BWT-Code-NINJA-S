import streamlit as st
import pandas as pd
import numpy as np
import io
import plotly.express as px
import plotly.graph_objects as go
from backend.data_processing import load_dataset, add_time_features
from backend.forecast_engine import train_and_forecast
from backend.waste_detection_engine import detect_anomalies
from backend.optimization_engine import optimize_peaks
from backend.carbon_simulator import compute_carbon_metrics
from backend.recommendation_engine import generate_recommendations

st.set_page_config(page_title="EnergiAI", layout="wide")
st.markdown(
    """
    <div style="padding:20px;border-radius:12px;background:linear-gradient(90deg,#1e8e3e,#34a853);color:white;margin-bottom:16px;">
      <div style="font-size:28px;font-weight:700;">🌍 EnergiAI – Autonomous Climate Optimization Engine</div>
      <div style="font-size:14px;opacity:0.95;">AI-powered system for detecting energy waste and optimizing climate impact.</div>
    </div>
    """,
    unsafe_allow_html=True
)

uploaded = st.file_uploader("Upload energydata_complete.csv", type=["csv"])
use_sample = st.checkbox("Use sample data preview", False)
if uploaded is None and not use_sample:
    st.stop()

if uploaded is not None:
    df = load_dataset(uploaded)
else:
    sample = pd.DataFrame({
        "date": pd.date_range(end=pd.Timestamp.now().floor("min"), periods=24*6, freq="10min"),
        "Appliances": np.random.randint(50, 400, size=24*6)
    })
    df = load_dataset(io.StringIO(sample.to_csv(index=False)))

df = add_time_features(df)
model_choice = st.selectbox("Forecasting model", ["Linear Regression", "Random Forest"])
baseline_df, forecast_df = train_and_forecast(df, model_type="rf" if model_choice == "Random Forest" else "lr")
anomaly_df = detect_anomalies(df)
optimized_df = optimize_peaks(df)
metrics = compute_carbon_metrics(df["energy_kwh"], optimized_df["optimized_energy"])

st.subheader("Top KPIs")
colA, colB, colC, colD, colE = st.columns(5)
with colA:
    st.metric("⚡ Baseline Energy (kWh)", f"{metrics['baseline_kwh']:.2f}")
with colB:
    st.metric("⚡ Optimized Energy (kWh)", f"{metrics['optimized_kwh']:.2f}")
with colC:
    st.metric("💡 Energy Saved (kWh)", f"{metrics['energy_saved_kwh']:.2f}")
with colD:
    st.metric("🌿 Carbon Saved (kg)", f"{metrics['carbon_saved_kg']:.2f}")
with colE:
    st.metric("🏆 Efficiency Score", f"{metrics['efficiency_score']:.0f} / 100")
if metrics["efficiency_score"] >= 90:
    st.success("Status: Excellent")
elif metrics["efficiency_score"] >= 70:
    st.info("Status: Efficient")
else:
    st.warning("Status: Needs Improvement")

col1, col2 = st.columns(2)
with col1:
    st.subheader("📊 Energy Optimization Comparison")
    chart_df = pd.DataFrame({
        "timestamp": df["timestamp"],
        "baseline_kwh": df["energy_kwh"],
        "optimized_kwh": optimized_df["optimized_energy"]
    }).set_index("timestamp")
    st.line_chart(chart_df)
with col2:
    st.subheader("Energy Forecast Trend")
    st.line_chart(forecast_df.set_index("timestamp"))

st.subheader("Anomaly Detection")
waste = anomaly_df[anomaly_df["anomaly"] == 1]
if not waste.empty:
    ts_alert = waste["timestamp"].iloc[-1]
    st.warning(f"⚠ Unusual energy spike detected at {ts_alert:%H:%M}")
st.dataframe(waste.tail(50))

st.subheader("Climate Impact")
colX, colY, colZ = st.columns(3)
with colX:
    st.metric("Energy Saved %", f"{metrics['energy_saved_pct']:.2f}%")
with colY:
    st.metric("Carbon Reduced (kg)", f"{metrics['carbon_saved_kg']:.2f}")
with colZ:
    st.metric("🌳 Trees Equivalent", f"{metrics['trees_equivalent']:.2f}")
colZ2a, colZ2b = st.columns(2)
with colZ2a:
    st.metric("🔋 Phone Charging Equivalent", f"{metrics['phone_charging_equiv']:.0f}")

st.subheader("Peak Energy Alert")
peak_hour = int(df.groupby("hour")["energy_kwh"].mean().idxmax())
st.warning(f"⚠ Peak Energy Detected at {peak_hour:02d}:00")
if peak_hour >= 10 and peak_hour <= 18:
    st.write("Suggest: Reduce appliance usage or reschedule energy-intensive tasks.")

st.subheader("AI Recommendations")
recs = generate_recommendations(anomaly_df, optimized_df)
st.table(recs)

st.subheader("What-If Simulation")
reduction_pct = st.slider("Reduction percentage", 5, 30, 15, 1)
sim_df = optimize_peaks(df, top_fraction=0.10, reduction_ratio=reduction_pct / 100.0)
sim_metrics = compute_carbon_metrics(df["energy_kwh"], sim_df["optimized_energy"])
colS1, colS2, colS3, colS4 = st.columns(4)
with colS1:
    st.metric("Sim Optimized kWh", f"{sim_metrics['optimized_kwh']:.2f}")
with colS2:
    st.metric("Sim Energy Saved %", f"{sim_metrics['energy_saved_pct']:.2f}%")
with colS3:
    st.metric("Sim Carbon Saved (kg)", f"{sim_metrics['carbon_saved_kg']:.2f}")
with colS4:
    st.metric("Sim Trees Equivalent 🌳", f"{sim_metrics['trees_equivalent']:.2f}")
st.metric("Sim Efficiency Score", f"{sim_metrics['efficiency_score']:.0f} / 100")
if sim_metrics["efficiency_score"] >= 90:
    st.success("Status: Excellent")
elif sim_metrics["efficiency_score"] >= 70:
    st.info("Status: Efficient")
else:
    st.warning("Status: Needs Optimization")
