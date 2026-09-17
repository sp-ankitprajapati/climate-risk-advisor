# Climate Risk AI Advisor

An AI agent that generates climate-risk reports grounded in real historical
weather data — built to bridge climate science and software engineering.

## What it does
Enter any location's coordinates → the agent fetches 15 years of real daily
weather data, runs a statistical trend and anomaly analysis, then uses Gemini
AI with function-calling to write a structured climate risk report — the same
type of deliverable ESG consulting teams produce for corporate clients.

## How it works
1. **Data layer** — fetches daily temperature and rainfall from Open-Meteo API (free, no key needed)
2. **Analysis layer** — computes yearly trend using linear regression, flags anomalous years using standard deviation
3. **Agent layer** — Gemini 3.0 Flash with tool-calling autonomously fetches data and runs analysis before writing a grounded report
4. **Interface** — Streamlit web app, deployable for free on Streamlit Cloud

## Tech stack
Python · pandas · numpy · Google Gemini 3.0 Flash API · Streamlit

## Setup
```bash
git clone https://github.com/yourusername/climate-risk-advisor
cd climate-risk-advisor
pip install -r requirements.txt
cp .env.example .env
# Add your free Gemini API key from https://aistudio.google.com
streamlit run app.py
```

## What I'd add with more time
- Multi-location comparison side by side
- Prophet model for future-year projections
- PDF export for actual ESG filings
- Integration with carbon emissions API for Scope 1/2/3 estimates
