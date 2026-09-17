import pandas as pd
import numpy as np

def analyze_trend(df):
    """
    Takes the climate DataFrame and returns a dictionary summarizing:
    - yearly average temperature and rainfall
    - whether temperature is trending up/down, and by how much
    - which years were unusually extreme (anomalies)
    """
    yearly = df.groupby("year").agg({
        "temperature": "mean",
        "rainfall": "sum"
    }).reset_index()

    # Linear regression: fits a straight line through yearly temps
    years = yearly["year"].values
    temps = yearly["temperature"].values
    slope, intercept = np.polyfit(years, temps, 1)

    # Anomaly detection: flag years where rainfall was more than
    # 1.5 standard deviations away from the long-term average
    rainfall_mean = yearly["rainfall"].mean()
    rainfall_std = yearly["rainfall"].std()
    yearly["rainfall_anomaly"] = (
        (yearly["rainfall"] - rainfall_mean).abs() > 1.5 * rainfall_std
    )
    anomaly_years = yearly[yearly["rainfall_anomaly"]]["year"].tolist()

    return {
        "yearly_data": yearly.to_dict(orient="records"),
        "temperature_trend_per_year": round(slope, 4),
        "avg_rainfall_mm": round(rainfall_mean, 1),
        "anomaly_years": anomaly_years
    }

if __name__ == "__main__":
    df = pd.read_csv("indore_climate.csv")
    result = analyze_trend(df)
    print(result)
