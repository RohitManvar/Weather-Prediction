import joblib
from rules import weather_prediction

# Load trained models
temp_model = joblib.load("temp_model.pkl")
rain_model = joblib.load("rain_model.pkl")

# Sample input (you can change values)
humidity = 72
wind_speed = 7
pressure = 1011

X_input = [[humidity, wind_speed, pressure]]

# Predictions
pred_temp = temp_model.predict(X_input)[0]
pred_rain = rain_model.predict(X_input)[0]

condition = weather_prediction(pred_temp, humidity, pred_rain)

# Output
print("Weather Prediction Result")
print("----------------------------")
print("Temperature:", round(pred_temp, 2), "°C")
print("Rain:", "Yes" if pred_rain == 1 else "No")
print("Condition:", condition)
