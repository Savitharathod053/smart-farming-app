import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import requests

# Page settings
st.set_page_config(page_title="Smart Farming", page_icon="🌾")

# Title
st.title("🌾 Smart Farming Assistant")

# Load dataset
data = pd.read_csv("Crop_recommendation.csv")

X = data.drop("label", axis=1)
y = data["label"]

model = RandomForestClassifier()
model.fit(X, y)

# City input
city = st.text_input("Enter your city")

# Weather function
def get_weather(city):
    api_key = "1363cc7c140d05f8f8b6762ec443c244"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    res = requests.get(url).json()
    
    temp = res["main"]["temp"]
    humidity = res["main"]["humidity"]
    rainfall = res.get("rain", {}).get("1h", 100)
    
    return temp, humidity, rainfall

# Get weather
if city:
    try:
        temp, humidity, rainfall = get_weather(city)
        st.write(f"🌡️ Temperature: {temp} °C")
        st.write(f"💧 Humidity: {humidity} %")
        st.write(f"🌧️ Rainfall: {rainfall}")
    except:
        st.error("Invalid city")
        temp, humidity, rainfall = 25, 60, 100
else:
    temp, humidity, rainfall = 25, 60, 100

# Inputs
st.subheader("Enter Soil Details")

N = st.number_input("Nitrogen", 0, 150)
P = st.number_input("Phosphorus", 0, 150)
K = st.number_input("Potassium", 0, 150)
ph = st.slider("Soil pH", 0.0, 14.0, 6.5)

# Prediction
if st.button("🌱 Predict Crop"):
    values = [[N, P, K, temp, humidity, ph, rainfall]]
    result = model.predict(values)
    st.success(f"✅ Recommended Crop: {result[0]}")