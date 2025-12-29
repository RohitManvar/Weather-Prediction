def weather_prediction(temp,humidity,rain):
    if rain == 1 and humidity > 80:
        return "Rainy"
    elif temp > 32 and humidity < 60:
        return "Sunny"
    elif humidity > 70:
        return "Cloudy"
    else:
        return "Normal"