import streamlit as st
from agent import run_agent

st.set_page_config(
    page_title="Climate Risk AI Advisor",
    page_icon="🌍",
    layout="centered"
)

st.title("🌍 Climate Risk AI Advisor")
st.markdown(
    "Enter any location's coordinates to generate an **AI-powered climate risk report** "
    "grounded in real historical weather data (2010–2024)."
)
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    city = st.text_input("City name (for reference)", "Indore")
    latitude = st.number_input("Latitude", value=22.7196, format="%.4f")
with col2:
    st.markdown("#### Quick location lookup")
    st.markdown("""
    | City | Latitude | Longitude |
    |------|----------|-----------|
    | Hyderabad | 17.3850 | 78.4867 |
    | Mumbai | 19.0760 | 72.8777 |
    | Delhi | 28.6139 | 77.2090 |
    | Chennai | 13.0827 | 80.2707 |
    | Bengaluru | 12.9716 | 77.5946 |
    """)

longitude = st.number_input("Longitude", value=75.8577, format="%.4f")

st.markdown("---")

if st.button("🔍 Generate Climate Risk Report", use_container_width=True):
    with st.spinner("Fetching climate data and generating report... (this takes ~15 seconds)"):
        try:
            report = run_agent(
                f"Generate a detailed climate risk summary for {city} suitable for an ESG report.",
                latitude, longitude
            )
            st.success("Report generated successfully!")
            st.markdown("### 📄 Climate Risk Report")
            st.markdown(report)
            st.download_button(
                label="Download Report as .txt",
                data=report,
                file_name=f"{city}_climate_risk_report.txt",
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"Error generating report: {e}")
            st.info("Check that your GEMINI_API_KEY is set correctly in the .env file.")

st.markdown("---")
st.caption(
    "Data source: Open-Meteo Historical Weather API | "
    "AI: Google Gemini 3.6 Flash | "
    "Built with Python, pandas, numpy, Streamlit"
)
