import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

def train_and_forecast(df: pd.DataFrame, horizon_steps: int = 96, model_type: str = "lr") -> tuple[pd.DataFrame, pd.DataFrame]:
    ts = pd.to_datetime(df["timestamp"])
    X = pd.DataFrame({"hour": ts.dt.hour, "day": ts.dt.dayofweek, "weekday": (ts.dt.dayofweek <= 4).astype(int), "peak_hour": ((ts.dt.hour >= 10) & (ts.dt.hour <= 18) & (ts.dt.dayofweek <= 4)).astype(int)})
    X = pd.get_dummies(X, columns=["hour", "day"], drop_first=False)
    y = df["energy_kwh"].values
    if model_type == "rf":
        model = RandomForestRegressor(n_estimators=120, random_state=42)
    else:
        model = LinearRegression()
    model.fit(X, y)
    step = ts.diff().median()
    if pd.isna(step):
        step = pd.Timedelta(minutes=10)
    future_ts = pd.date_range(start=ts.iloc[-1] + step, periods=horizon_steps, freq=step)
    future_X = pd.DataFrame({"hour": future_ts.hour, "day": future_ts.dayofweek, "weekday": (future_ts.dayofweek <= 4).astype(int), "peak_hour": ((future_ts.hour >= 10) & (future_ts.hour <= 18) & (future_ts.dayofweek <= 4)).astype(int)})
    future_X = pd.get_dummies(future_X, columns=["hour", "day"], drop_first=False)
    future_X = future_X.reindex(columns=X.columns, fill_value=0)
    preds = model.predict(future_X)
    forecast_df = pd.DataFrame({"timestamp": future_ts, "forecast_kwh": preds})
    baseline_df = pd.DataFrame({"timestamp": ts, "baseline_kwh": model.predict(X)})
    return baseline_df, forecast_df
