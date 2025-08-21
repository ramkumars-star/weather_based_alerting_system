import streamlit as st
import requests

API_KEY = 'b053a728674d5cb56ec19eab5d610afc'

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def analyze_weather(weather_data):
    if not weather_data:
        return ["No weather data available."]
    main = weather_data['main']
    weather = weather_data['weather'][0]   # Fixed: Accessing first dictionary in list
    temp = main['temp']
    rain = weather_data.get('rain', {}).get('1h', 0)
    alerts = []

    if rain > 5:
        alerts.append(f"Heavy rainfall expected: {rain}mm in last hour.")
    if temp > 40:
        alerts.append("Extreme heat alert! Temperature above 40°C.")
    if temp < 5:
        alerts.append("Frost alert! Temperature below 5°C.")

    if not alerts: 
        alerts.append("Weather conditions are normal.")
    return alerts

st.title("Weather-Based Alerting System")

city = st.text_input("Enter your city:")

if st.button("Get Weather Alert"):
    if city:
        weather = get_weather(city)
        alerts = analyze_weather(weather)
        for alert in alerts:
            st.warning(alert)
    else:
        st.error("Please enter a city name.")

