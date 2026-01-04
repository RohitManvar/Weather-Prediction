import streamlit as st
import requests
import joblib
from rules import weather_prediction
from forecast import generate_5_day_forecast

API_KEY = "" 
st.set_page_config(page_title="Weather Forecast", layout="centered")
st.title("🌦️ Weather Prediction System (ML + API)")

city = st.text_input(
    "Enter City Name",
    placeholder="e.g. Tokyo, Vadodara, etc."
)

if st.button("Get Weather"):
    if city.strip() == "":
        st.warning("Please enter a city name")
    else:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # API values
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            pressure = data["main"]["pressure"]

            # Load ML models
            temp_model = joblib.load("temp_model.pkl")
            rain_model = joblib.load("rain_model.pkl")

            # Prepare input
            X_input = [[humidity, wind_speed, pressure]]

            # Predictions
            pred_temp = temp_model.predict(X_input)[0]
            pred_rain = rain_model.predict(X_input)[0]

            # Rule-based condition
            condition = weather_prediction(pred_temp, humidity, pred_rain)

            # 5-day forecast
            forecast = generate_5_day_forecast(pred_temp)

            # UI output
            st.subheader(f"📍 {city}")
            st.metric("🌡️ Predicted Temperature (°C)", f"{pred_temp:.2f}")
            st.metric("🌧️ Rain", "Yes" if pred_rain == 1 else "No")
            st.metric("☁️ Condition", condition)

            st.subheader("📅 5-Day Forecast")
            for i, t in enumerate(forecast, 1):
                st.write(f"Day {i}: {t:.2f} °C")

        else:
            st.error("City not found")
