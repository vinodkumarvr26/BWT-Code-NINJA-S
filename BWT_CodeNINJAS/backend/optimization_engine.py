import pandas as pd

def optimize_peaks(df: pd.DataFrame, top_fraction: float = 0.10, reduction_ratio: float = 0.15) -> pd.DataFrame:
    out = df.copy()
    n = len(out)
    k = max(1, int(n * top_fraction))
    idx = out["energy_kwh"].nlargest(k).index
    out["optimized_energy"] = out["energy_kwh"]
    out.loc[idx, "optimized_energy"] = out.loc[idx, "optimized_energy"] * (1 - reduction_ratio)
    return out
