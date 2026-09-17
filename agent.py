import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from data import get_climate_data
from analysis import analyze_trend

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Store fetched data between tool calls
_fetched_df = None

def fetch_climate_data(latitude: float, longitude: float) -> str:
    """
    Fetch historical daily temperature and rainfall data
    for a location given latitude and longitude coordinates.

    Args:
        latitude: Latitude of the location.
        longitude: Longitude of the location.
    """
    global _fetched_df
    _fetched_df = get_climate_data(latitude, longitude)
    return f"Successfully fetched {len(_fetched_df)} days of climate data for coordinates ({latitude}, {longitude})."

def run_trend_analysis() -> str:
    """
    Analyze the fetched climate data to find the temperature
    trend rate per year and identify rainfall anomaly years.
    Call this only after fetch_climate_data has been called.
    """
    global _fetched_df
    if _fetched_df is None:
        return "Error: No data fetched yet. Please call fetch_climate_data first."
    result = analyze_trend(_fetched_df)
    return json.dumps(result)

def run_agent(user_query, latitude, longitude):
    """
    Runs the Gemini agent with automatic function calling.
    The model decides when to call fetch_climate_data and
    run_trend_analysis before writing the final report.
    """
    global _fetched_df
    _fetched_df = None  # reset for each new query

    full_query = (
        f"{user_query} "
        f"Location coordinates: latitude={latitude}, longitude={longitude}."
    )

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=full_query,
        config=types.GenerateContentConfig(
            tools=[fetch_climate_data, run_trend_analysis],
            system_instruction=(
                "You are an expert climate risk analyst producing ESG-grade reports. "
                "When asked about climate risk for a location, you MUST: "
                "1) First call fetch_climate_data with the provided coordinates. "
                "2) Then call run_trend_analysis to get trend statistics. "
                "3) Only then write a structured climate risk report grounded in the real numbers. "
                "Never make up or estimate climate statistics — always use the tool results."
            )
        )
    )

    return response.text

if __name__ == "__main__":
    report = run_agent(
        "Generate a detailed climate risk summary for this location suitable for an ESG report.",
        22.7196, 75.8577
    )
    print(report)
