import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor


def predict_expenses(expenses, days=30):
    if len(expenses) < 5:
        return None

    df = pd.DataFrame(expenses)

    df["Date"] = pd.to_datetime(df["Date"])
    df["Amount"] = pd.to_numeric(df["Amount"])

    daily = (
        df.groupby("Date")["Amount"]
        .sum()
        .reset_index()
    )

    daily["DayNumber"] = (
        daily["Date"] - daily["Date"].min()
    ).dt.days

    if len(daily) < 3:
        return None

    X = daily[["DayNumber"]]
    y = daily["Amount"]

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    future_days = np.arange(
        daily["DayNumber"].max() + 1,
        daily["DayNumber"].max() + days + 1
    ).reshape(-1, 1)

    predictions = model.predict(future_days)

    predictions = np.maximum(predictions, 0)

    return {
        "predicted_total": float(predictions.sum()),
        "daily_average": float(predictions.mean()),
        "days": days
    }