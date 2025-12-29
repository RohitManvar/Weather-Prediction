def generate_5_day_forecast(temp):
    forecast=[]
    for i in range(1,6):
        forecast.append(round(temp + (i * 0.5), 2))
    return forecast
    
