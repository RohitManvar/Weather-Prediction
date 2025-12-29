import pandas as pd 
from sklearn.linear_model import LinearRegression, LogisticRegression
import joblib

#Load Data
data = pd.read_csv("weather.csv")

x = data[['humidity', 'wind_speed', 'pressure']]
y_temp = data['temperature']
y_rain = data['rain']

#Temperature Regression Model
temp_model = LinearRegression()
temp_model.fit(x,y_temp)

#Rain Classification Model
rain_model = LogisticRegression()
rain_model.fit(x,y_rain)

#Save Models
joblib.dump(temp_model,"temp_model.pkl")
joblib.dump(rain_model,"rain_model.pkl")

print("Model Trained and Save Successfully")