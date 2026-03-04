import pandas as pd

def compute_carbon_metrics(baseline: pd.Series, optimized: pd.Series, emission_factor_kg_per_kwh: float = 0.82) -> dict:
    baseline_kwh = float(baseline.sum())
    optimized_kwh = float(optimized.sum())
    energy_saved_kwh = baseline_kwh - optimized_kwh
    energy_saved_pct = (energy_saved_kwh / baseline_kwh * 100) if baseline_kwh > 0 else 0.0
    baseline_co2_kg = baseline_kwh * emission_factor_kg_per_kwh
    optimized_co2_kg = optimized_kwh * emission_factor_kg_per_kwh
    carbon_saved_kg = baseline_co2_kg - optimized_co2_kg
    trees_equivalent = carbon_saved_kg / 21.0
    phone_charging_equiv = (energy_saved_kwh / 0.005) if energy_saved_kwh > 0 else 0.0
    efficiency_score = 100.0 - ((optimized_kwh / baseline_kwh) * 100.0) if baseline_kwh > 0 else 0.0
    return {
        "baseline_kwh": baseline_kwh,
        "optimized_kwh": optimized_kwh,
        "energy_saved_kwh": energy_saved_kwh,
        "energy_saved_pct": energy_saved_pct,
        "baseline_co2_kg": baseline_co2_kg,
        "optimized_co2_kg": optimized_co2_kg,
        "carbon_saved_kg": carbon_saved_kg,
        "trees_equivalent": trees_equivalent,
        "phone_charging_equiv": phone_charging_equiv,
        "efficiency_score": efficiency_score,
    }
