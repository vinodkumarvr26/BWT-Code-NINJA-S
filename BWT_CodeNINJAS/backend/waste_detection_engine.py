import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(df: pd.DataFrame, contamination: float = 0.05) -> pd.DataFrame:
    ts = pd.to_datetime(df["timestamp"])
    X = pd.DataFrame({"energy_kwh": df["energy_kwh"], "hour": ts.dt.hour, "day": ts.dt.dayofweek})
    model = IsolationForest(n_estimators=200, contamination=contamination, random_state=42)
    scores = model.fit_predict(X)
    out = df.copy()
    out["anomaly"] = (scores == -1).astype(int)
    return out
