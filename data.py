import requests
import pandas as pd

def get_climate_data(latitude, longitude, start_date="2010-01-01", end_date="2024-12-31"):
    """
    Fetches daily max temperature and rainfall for a location
    from the free Open-Meteo historical weather API.
    Returns a pandas DataFrame.
    """
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_max,precipitation_sum",
        "timezone": "auto"
    }

    response = requests.get(url, params=params)
    data = response.json()

    df = pd.DataFrame({
        "date": data["daily"]["time"],
        "temperature": data["daily"]["temperature_2m_max"],
        "rainfall": data["daily"]["precipitation_sum"]
    })
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year

    return df

if __name__ == "__main__":
    df = get_climate_data(22.7196, 75.8577)
    print(df.head())
    df.to_csv("indore_climate.csv", index=False)
    print(f"Saved {len(df)} rows to indore_climate.csv")
