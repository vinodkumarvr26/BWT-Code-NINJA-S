import pandas as pd

def generate_recommendations(df_anomaly: pd.DataFrame, df_optimized: pd.DataFrame) -> pd.DataFrame:
    recs = []
    if df_anomaly["anomaly"].sum() > 0:
        recs.append("Investigate anomaly spikes")
    baseline_total = float(df_optimized["energy_kwh"].sum())
    optimized_total = float(df_optimized["optimized_energy"].sum()) if "optimized_energy" in df_optimized.columns else baseline_total
    if optimized_total < baseline_total:
        recs.append("Reduce AC usage during peak hours")
        recs.append("Shift high energy operations to off-peak times")
    if len(recs) == 0:
        recs.append("Maintain current operations; no significant waste detected")
    return pd.DataFrame({"recommendation": recs})
