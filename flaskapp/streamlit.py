import streamlit as st
import requests
import json

st.title("Power Factor Prediction")
st.subheader("this project aims to predict the next power factor based on previous factors.")

sample_data = {"Voltage": 234.4, "Global_intensity" : 20.3, "apparent_power" : 4.4177616419, "Energy_kWh" : 0.073213, "hour" : 6, "minutes" : 30, "pref_power_factor" : 0.94, "mean_power_factor_3" : 0.90}




if 'clicked' not in st.session_state:
    st.session_state.clicked = {1:False}

def clicked(button):
    st.session_state.clicked[button] = True

st.button("Let's get started", on_click=clicked, args=[1])

if st.session_state.clicked[1]:

    feature_1 = st.slider("Voltage Value", value=234.4, min_value=0.0, max_value=1000.0)
    feature_2 = st.slider("Global Intensity:", value=20.3, min_value=0.0, max_value=150.0)
    feature_3 = st.number_input("Apparent Power", value=4.41, min_value=0.0, max_value=50.0)
    feature_4 = st.number_input("Energy in kWh", value=0.073, min_value=0.0, max_value=1.0)
    feature_5 = st.slider("Hour", value=6, max_value=24)
    feature_6 = st.slider("Minutes",value=30, max_value=60, step=15)
    feature_7 = st.number_input("Pref Power Factor", value=0.94, min_value=0.0, max_value=1.0)
    feature_8 = st.number_input("Mean Power factor on the last 3 days", min_value=0.0, max_value=1.0, value=0.9)

    if st.button("Get Prediction"):
        input_data = {
            "features": [feature_1, feature_2, feature_3, feature_4, feature_5, feature_6, feature_7, feature_8]
        }

        response = requests.post("http://127.0.0.1:5000/predict", json=input_data)

        if response.status_code == 200:
            result = response.json()
            result_str = json.dumps(result, indent=4)
            st.success(f"Prediction: {result['prediction']}") 
            st.download_button("Download the results", result_str, 'results.txt', 'text/plain', key='download-text')
            
        else:
            st.error("Failed to get prediction from model API")

