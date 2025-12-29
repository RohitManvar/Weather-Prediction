import streamlit as st 
import requests
import joblib
from rules import weather_prediction
from forecast import generate_5_day_forecast

API_KEY = ""

st.set_page_config(page_title="Weather Forecast", layout="centered")
st.title("Weather Prediction System (ML + API)")

city = st.text("Enter City Name")

if city:
    url =""
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        pressure = data['main']['pressure']

        temp_model = joblib.load("temp_model.pkl")
        rain_model = joblib.load("rain_model.pkl")

        X_input = [[humidity, wind_speed, pressure]]

        pred_temp = temp_model.predict(X_input)[0]
        pred_rain = rain_model.predict(X_input)[0]
        humidity = data['main','humidity']

        condition = weather_prediction(pred_temp,humidity,pred_rain)
        forecast = generate_5_day_forecast(pred_temp)

        st.subheader(f"{city}")

        st.subheader(f"📍 {city}")
        st.write(f"🌡️ Temperature: **{pred_temp:.2f} °C**")
        st.write(f"🌧️ Rain: **{'Yes' if pred_rain == 1 else 'No'}**")
        st.write(f"☁️ Condition: **{condition}**")

        st.subheader("📅 5-Day Forecast")
        for i, t in enumerate(forecast, 1):
            st.write(f"Day {i}: {t} °C")
    else:
        st.error("City not found")