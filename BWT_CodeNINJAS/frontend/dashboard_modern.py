import streamlit as st
import pandas as pd
import numpy as np
import io
import plotly.graph_objects as go
from backend.data_processing import load_dataset, add_time_features
from backend.forecast_engine import train_and_forecast
from backend.waste_detection_engine import detect_anomalies
from backend.optimization_engine import optimize_peaks
from backend.carbon_simulator import compute_carbon_metrics
from backend.recommendation_engine import generate_recommendations

st.set_page_config(page_title="EnergiAI", layout="wide")
st.title("EnergiAI – Autonomous Climate Optimization Engine")

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
buildings = ["Library", "Hostel", "Academic Block", "Laboratory"]
if "building" not in df.columns:
    df["building"] = np.random.choice(buildings, size=len(df))
filters = st.columns([2, 2, 3])
with filters[0]:
    building = st.selectbox("🏢 Select Building / Zone", buildings)
df_b = df[df["building"] == building].reset_index(drop=True)
df_b = add_time_features(df_b)
with filters[1]:
    model_choice = st.selectbox("🧠 Forecasting model", ["Linear Regression", "Random Forest"])
baseline_df, forecast_df = train_and_forecast(df_b, model_type="rf" if model_choice == "Random Forest" else "lr")
anomaly_df = detect_anomalies(df_b)
optimized_df = optimize_peaks(df_b)
metrics = compute_carbon_metrics(df_b["energy_kwh"], optimized_df["optimized_energy"])
cost_saved = metrics["energy_saved_kwh"] * 8.0

st.subheader("Top Metrics")
st.caption("Key operational KPIs for the selected building/zone.")
ca, cb, cc, cd, ce = st.columns(5)
with ca:
    st.metric("Baseline Energy (kWh)", f"{metrics['baseline_kwh']:.2f}")
with cb:
    st.metric("Optimized Energy (kWh)", f"{metrics['optimized_kwh']:.2f}")
with cc:
    st.metric("Energy Saved (kWh)", f"{metrics['energy_saved_kwh']:.2f}")
with cd:
    st.metric("Carbon Saved (kg)", f"{metrics['carbon_saved_kg']:.2f}")
with ce:
    st.metric("Cost Savings (₹)", f"{cost_saved:.2f}")
if metrics["efficiency_score"] >= 90:
    st.success("Status: Excellent")
elif metrics["efficiency_score"] >= 70:
    st.info("Status: Efficient")
else:
    st.warning("Status: Needs Improvement")

st.divider()
tab1, tab2, tab3, tab4 = st.tabs(["1️⃣ Energy Analysis", "2️⃣ Optimization Insights", "3️⃣ Climate Impact", "4️⃣ Simulation Lab"])
with tab1:
    st.subheader("Energy Consumption Trend")
    st.caption("Baseline energy usage for the selected building/zone.")
    trend_df = df_b[["timestamp", "energy_kwh"]].set_index("timestamp")
    st.line_chart(trend_df)
    mean_e = float(df_b["energy_kwh"].mean())
    std_e = float(df_b["energy_kwh"].std())
    threshold = mean_e + 2.0 * std_e
    if (df_b["energy_kwh"] > threshold).any():
        st.warning("⚠ Predicted Peak Energy Demand Detected")
        peak_hour = int(df_b.groupby("hour")["energy_kwh"].mean().idxmax())
        peak_value = float(df_b["energy_kwh"].max())
        st.metric("Peak Usage Hour", f"{peak_hour:02d}:00")
        st.metric("Peak Consumption Value (kWh)", f"{peak_value:.2f}")

with tab2:
    st.subheader("Energy Optimization Analysis")
    st.caption("Before vs after optimization for peak demand reduction.")
    chart_df = pd.DataFrame({
        "timestamp": df_b["timestamp"],
        "Baseline": df_b["energy_kwh"],
        "Optimized": optimized_df["optimized_energy"]
    })
    st.line_chart(chart_df.set_index("timestamp"))
    peak_hour = int(df_b.groupby("hour")["energy_kwh"].mean().idxmax())
    st.warning(f"⚠ Peak Energy Usage Detected at Hour {peak_hour:02d}")

with tab3:
    st.subheader("Carbon Impact")
    colX, colY, colZ = st.columns(3)
    with colX:
        st.metric("Energy Saved %", f"{metrics['energy_saved_pct']:.2f}%")
    with colY:
        st.metric("Carbon Reduced (kg)", f"{metrics['carbon_saved_kg']:.2f}")
    with colZ:
        st.metric("🌳 Trees Equivalent", f"{metrics['trees_equivalent']:.2f}")
    c1, c2 = st.columns(2)
    with c1:
        st.metric("🔋 Phone Charging Equivalent", f"{metrics['phone_charging_equiv']:.0f}")
    st.divider()
    recs = generate_recommendations(anomaly_df, optimized_df)
    st.subheader("AI Optimization Recommendations")
    st.table(recs)

with tab4:
    st.subheader("Simulation Lab")
    reduction_pct = st.slider("Simulated energy reduction (%)", 5, 30, 15, 1)
    sim_df = optimize_peaks(df_b, top_fraction=0.10, reduction_ratio=reduction_pct / 100.0)
    sim_metrics = compute_carbon_metrics(df_b["energy_kwh"], sim_df["optimized_energy"])
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.metric("Sim Optimized kWh", f"{sim_metrics['optimized_kwh']:.2f}")
    with s2:
        st.metric("Sim Energy Saved %", f"{sim_metrics['energy_saved_pct']:.2f}%")
    with s3:
        st.metric("Sim Carbon Saved (kg)", f"{sim_metrics['carbon_saved_kg']:.2f}")
    with s4:
        st.metric("Sim Trees Equivalent 🌳", f"{sim_metrics['trees_equivalent']:.2f}")
    st.metric("Sim Efficiency Score", f"{sim_metrics['efficiency_score']:.0f} / 100")

st.divider()
st.subheader("Current Energy Monitoring")
latest = df_b.iloc[-1]
st.metric("Current Energy Consumption (kWh)", f"{latest['energy_kwh']:.2f}")
st.metric("Current Building", building)

st.divider()
st.subheader("Appliance / Area Energy Distribution")
categories = ["HVAC System", "Lighting", "Laboratory Equipment", "Servers"]
rng = np.random.default_rng(42)
shares = rng.dirichlet(np.ones(len(categories)), size=len(df_b))
totals = (shares * df_b["energy_kwh"].to_numpy()[:, None]).sum(axis=0)
appliance_df = pd.DataFrame({"Appliance": categories, "kWh": totals}).set_index("Appliance")
st.bar_chart(appliance_df)
current_appliance = categories[int(np.argmax(shares[-1]))]
st.metric("Current Appliance", current_appliance)

st.divider()
st.subheader("Carbon Footprint Difference")
st.metric("Carbon Emission Before Optimization (kg)", f"{metrics['baseline_co2_kg']:.2f}")
st.metric("Carbon Emission After Optimization (kg)", f"{metrics['optimized_co2_kg']:.2f}")
st.metric("Total Carbon Reduction (kg)", f"{metrics['carbon_saved_kg']:.2f}")
st.metric("Trees Saved 🌳", f"{(metrics['carbon_saved_kg']/21.0):.2f}")

st.divider()
st.subheader("Sustainability Scorecard")
efficiency_score = metrics["efficiency_score"]
carbon_score = (metrics["carbon_saved_kg"] / metrics["baseline_co2_kg"] * 100.0) if metrics["baseline_co2_kg"] > 0 else 0.0
cost_score = (cost_saved / (metrics["baseline_kwh"] * 8.0) * 100.0) if metrics["baseline_kwh"] > 0 else 0.0
overall_score = (efficiency_score + carbon_score + cost_score) / 3.0
colS = st.columns(3)
colS[0].metric("Energy Efficiency Score", f"{efficiency_score:.0f} / 100")
colS[1].metric("Carbon Reduction Score", f"{carbon_score:.0f} / 100")
colS[2].metric("Cost Efficiency Score", f"{cost_score:.0f} / 100")
st.metric("Overall Sustainability Score", f"{overall_score:.0f} / 100")
st.progress(min(max(overall_score / 100.0, 0.0), 1.0))

st.divider()
st.subheader("Energy Usage Analysis")
peak_hour = int(df_b.groupby("hour")["energy_kwh"].mean().idxmax())
st.write(f"Peak Energy Usage occurred around {peak_hour:02d}:00")
top_building = df.groupby("building")["energy_kwh"].sum().idxmax()
st.write(f"Highest energy usage observed in {top_building}.")

extra_recs = [
    "Reduce HVAC usage during peak afternoon hours",
    "Shift heavy equipment usage to off-peak periods",
    "Optimize lighting during daylight hours"
]
st.subheader("AI Optimization Recommendations")
combined_recs = pd.DataFrame({"recommendation": list(dict.fromkeys(list(generate_recommendations(anomaly_df, optimized_df)["recommendation"]) + extra_recs))})
st.table(combined_recs)

st.divider()
st.markdown("---")
st.write("Built by: Vinod Kumar, Srishti B S, Devipriya S, Devipriya S and Yashaswini M")
