import streamlit as st
import requests
from twilio.rest import Client
import os

# Set your API keys below or configure them as environment variables
API_KEY = os.getenv('b053a728674d5cb56ec19eab5d610afc') or 'b053a728674d5cb56ec19eab5d610afc'
TWILIO_ACCOUNT_SID = os.getenv('ACf9ce30b42bad63db68939968aef37f20') or 'ACf9ce30b42bad63db68939968aef37f20'
TWILIO_AUTH_TOKEN = os.getenv('a5978a026ce3c021cb4a9d6af69f34c9') or 'a5978a026ce3c021cb4a9d6af69f34c9'
TWILIO_PHONE_NUMBER = os.getenv('+12764214139') or '+12764214139'  # Your Twilio number

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city.strip()}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def analyze_weather(weather_data):
    if not weather_data:
        return ["No weather data available."]
    main = weather_data['main']
    temp = main['temp']
    rain = weather_data.get('rain', {}).get('1h', 0)
    
    st.write(f"Temperature (°C): {temp}")
    st.write(f"Rainfall in last 1 hour (mm): {rain}")
    
    alerts = []
    if rain > 0:
        alerts.append(f"Rainfall expected: {rain}mm in last hour.")
    if temp > 30:
        alerts.append("Heat alert! Temperature above 30°C.")
    if temp < 20:
        alerts.append("Cold alert! Temperature below 20°C.")
    if not alerts:
        alerts.append("Weather conditions are normal.")
    return alerts

translations = {
    "Rainfall expected:": {
        "Hindi": "बारिश होने की संभावना है:",
        "Spanish": "Se espera lluvia:",
        "Tamil": "மழை எதிர்பார்க்கப்படுகிறது:"
    },
    "Heat alert! Temperature above 30°C.": {
        "Hindi": "गर्मी चेतावनी! तापमान 30°C से ऊपर है।",
        "Spanish": "Alerta de calor! Temperatura por encima de 30°C.",
        "Tamil": "வெப்ப எச்சரிக்கை! வெப்பநிலை 30°C க்கு மேல்."
    },
    "Cold alert! Temperature below 20°C.": {
        "Hindi": "ठंडी चेतावनी! तापमान 20°C से नीचे है।",
        "Spanish": "Alerta de frío! Temperatura por debajo de 20°C.",
        "Tamil": "குளிர்ச்சித் எச்சரிக்கை! வெப்பநிலை 20°C க்கு கீழே."
    },
    "Weather conditions are normal.": {
        "Hindi": "मौसम सामान्य है।",
        "Spanish": "Las condiciones del tiempo son normales.",
        "Tamil": "வானிலை நிலைமைகள் சாதாரணம்."
    },
    "No weather data available.": {
        "Hindi": "मौसम डेटा उपलब्ध नहीं है।",
        "Spanish": "Datos meteorológicos no disponibles.",
        "Tamil": "வானிலைத் தரவு கிடைக்கவில்லை."
    }
}

def translate_alerts(alerts, lang):
    translated = []
    for alert in alerts:
        for key, lang_dict in translations.items():
            if key in alert:
                alert = alert.replace(key, lang_dict.get(lang, key))
        translated.append(alert)
    return translated

def send_sms_alert(to_phone, message):
    client = Client('ACf9ce30b42bad63db68939968aef37f20', 'a5978a026ce3c021cb4a9d6af69f34c9')
    try:
        msg = client.messages.create(
            body=message,
            from_=+12764214139,
            to=to_phone
        )
        return msg.sid
    except Exception as e:
        return str(e)

st.title("Weather-Based Alerting System for Multiple Cities")

language = st.selectbox("Select Language", ["English", "Hindi", "Spanish", "Tamil"])

city_input = st.text_area("Enter city names separated by commas (e.g., Chennai, Delhi, Mumbai):")
phone_number = st.text_input("Enter your phone number with country code (e.g., +919876543210):")

if st.button("Get Weather Alerts"):
    if city_input.strip():
        cities = [c.strip() for c in city_input.split(",") if c.strip()]
        all_alerts_sms = []
        for city in cities:
            st.subheader(f"Alerts for {city}")
            weather = get_weather(city)
            alerts = analyze_weather(weather)
            translated_alerts = translate_alerts(alerts, language)
            for alert in translated_alerts:
                st.warning(alert)
            all_alerts_sms.append(f"{city}:\n" + "\n".join(translated_alerts))
        
        if phone_number:
            sms_message = "\n\n".join(all_alerts_sms)
            result = send_sms_alert(phone_number, sms_message)
            if result and not result.startswith("Error"):
                st.success(f"SMS sent successfully! Message SID: {result}")
            else:
                st.error(f"Failed to send SMS: {result}")
        else:
            st.info("Enter a phone number to receive SMS alerts.")
    else:
        st.error("Please enter at least one city name.")


