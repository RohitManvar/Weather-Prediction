import streamlit as st
import requests
import joblib
import matplotlib.pyplot as plt
from rules import weather_prediction
from forecast import generate_5_day_forecast

# ==============================
# CONFIG
# ==============================
API_KEY = "7babbacfc81d1aadba29fdde4aa6ea50"

st.set_page_config(
    page_title="Weather Forecast",
    layout="centered"
)

# ==============================
# CUSTOM CSS
# ==============================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

h1, h2, h3 {
    color: #38B2AC;
}

input {
    border-radius: 10px !important;
}

.stButton>button {
    background-color: #38B2AC;
    color: black;
    font-weight: bold;
    border-radius: 10px;
    height: 45px;
    width: 100%;
}

.stButton>button:hover {
    background-color: #2dd4bf;
}

[data-testid="metric-container"] {
    background-color: #112240;
    border-radius: 12px;
    padding: 15px;
    color: white;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
}

section[data-testid="stSidebar"] {
    background-color: #0b1c2d;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# TITLE
# ==============================
st.title("🌦️ Weather Prediction")
st.caption("ML + Rule-based Logic + Live Weather API")

# ==============================
# AUTO LOCATION DETECTION
# ==============================
def get_user_city():
    try:
        res = requests.get("https://ipapi.co/json/").json()
        return res.get("city")
    except:
        return None

auto_city = get_user_city()

# ==============================
# LOAD MODELS (CACHED)
# ==============================
@st.cache_resource
def load_models():
    return joblib.load("temp_model.pkl"), joblib.load("rain_model.pkl")

temp_model, rain_model = load_models()

# ==============================
# WEATHER ICON
# ==============================
def get_icon(condition):
    condition = condition.lower()
    if "rain" in condition:
        return "🌧️"
    elif "cloud" in condition:
        return "☁️"
    elif "sun" in condition or "clear" in condition:
        return "☀️"
    else:
        return "🌡️"

# ==============================
# USER INPUT
# ==============================
city = st.text_input(
    "Enter City Name",
    value=auto_city if auto_city else "",
    placeholder="e.g. Tokyo, Vadodara"
)

# ==============================
# BUTTON ACTION
# ==============================
if st.button("Get Weather"):
    if city.strip() == "":
        st.warning("Please enter a city name")
    else:
        with st.spinner("Fetching live weather & predictions..."):
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                # API values
                humidity = data["main"]["humidity"]
                wind_speed = data["wind"]["speed"]
                pressure = data["main"]["pressure"]

                # ML input
                X_input = [[humidity, wind_speed, pressure]]

                # Predictions
                pred_temp = temp_model.predict(X_input)[0]
                pred_rain = rain_model.predict(X_input)[0]

                # Rule-based condition
                condition = weather_prediction(pred_temp, humidity, pred_rain)
                icon = get_icon(condition)

                # 5-day forecast
                forecast = generate_5_day_forecast(pred_temp)

                # ==============================
                # UI OUTPUT
                # ==============================
                st.subheader(f"{icon} Weather in {city}")

                col1, col2, col3 = st.columns(3)
                col1.metric("🌡 Temperature (°C)", f"{pred_temp:.2f}")
                col2.metric("🌧 Rain", "Yes" if pred_rain == 1 else "No")
                col3.metric("☁ Condition", condition)

                st.subheader("📅 5-Day Forecast")
                cols = st.columns(5)
                for i, (col, temp) in enumerate(zip(cols, forecast), 1):
                    col.metric(f"Day {i}", f"{temp:.1f} °C")

                st.subheader("📈 Temperature Trend")
                fig, ax = plt.subplots()
                ax.plot(range(1, 6), forecast, marker="o")
                ax.set_xlabel("Day")
                ax.set_ylabel("Temperature (°C)")
                ax.set_title("5-Day Temperature Forecast")
                st.pyplot(fig)

            else:
                st.error("City not found ")
