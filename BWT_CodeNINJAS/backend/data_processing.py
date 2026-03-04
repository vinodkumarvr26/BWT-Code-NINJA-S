import pandas as pd
import numpy as np

def load_dataset(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df["timestamp"] = pd.to_datetime(df["date"])
    df["energy_kwh"] = df["Appliances"] / 1000.0
    df = df[["timestamp", "energy_kwh"]].sort_values("timestamp").reset_index(drop=True)
    return df

def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    ts = pd.to_datetime(df["timestamp"])
    out = df.copy()
    out["hour"] = ts.dt.hour
    out["day"] = ts.dt.dayofweek
    out["weekday"] = (out["day"] <= 4).astype(int)
    out["peak_hour"] = ((out["hour"] >= 10) & (out["hour"] <= 18) & (out["weekday"] == 1)).astype(int)
    out["day_of_month"] = ts.dt.day
    return out
