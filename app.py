import streamlit as st
import pickle
import numpy as np
import base64

# Custom Styling
def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded_string}");
        background-size: cover;
    }}
    .cloud-box {{
        background-color: rgba(221, 243, 254, 0.6);
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 10px; 
    }}
    .subheading-box {{
        background-color: rgba(221, 243, 254, 0.6);
        padding: 10px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 35px; 
    }}
    .subsubheading-box {{
        background-color: rgba(254, 249, 215, 0.6);
        padding: 10px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        text-align: left;
        font-size: 16px;
        font-weight: bold;
        margin-bottom: -40px; 
    }}
    .subsubsubheading-box {{
        background-color: rgba(254, 249, 215, 0.6);
        padding: 10px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        text-align: left;
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 25px; 
        margin-top: 15px;
    }}
    .input-container {{
        background-color: rgba(230, 255, 230, 0.8);
        display: flex;
        flex-direction: column;
        padding: 8px; 
        border-radius: 10px;
        text-align: left;
        margin-top: -5px;
        margin-bottom: -45px;
    }}
    .output-block {{
        background-color: rgba(255, 200, 180, 0.8);
        padding: 8px; 
        border-radius: 10px;
        text-align: left;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Set background image
set_background("background.jpg")

# Load models
with open("crop_model.sav", "rb") as file:
    crop_model = pickle.load(file)

with open("fertilizer_model.sav", "rb") as file:
    fertilizer_model = pickle.load(file)

# Streamlit UI
st.markdown("<div class='cloud-box'>🌱 Crop & Fertilizer Prediction</div>", unsafe_allow_html=True)
st.markdown("<div class='subheading-box'>AI-based prediction for optimal farming</div>", unsafe_allow_html=True)

# Selection menu
st.markdown("<div class='subsubheading-box'>Choose Prediction Type</div>", unsafe_allow_html=True)
option = st.selectbox("", ["Crop Recommendation", "Fertilizer Recommendation"], key="prediction_type")

parameters = {
    "Crop Recommendation": ["Nitrogen (N)", "Phosphorus (P)", "Potassium (K)", "Temperature (°C)", "Humidity (%)", "pH Level", "Rainfall (mm)"],
    "Fertilizer Recommendation": ["Temperature (°C)", "Humidity (%)", "Soil Moisture (%)", "Soil Type", "Crop Type", "Nitrogen (N)", "Potassium (K)", "Phosphorus (P)"]
}

soil_mapping = {"Sandy": 0, "Loamy": 1, "Black": 2, "Red": 3, "Clayey": 4}
crop_mapping = {"Wheat": 0, "Maize": 1, "Barley": 2, "Pulses": 3, "Cotton": 4, "Tobacco": 5}

inputs = []
st.markdown(f"<div class='subsubsubheading-box'>{option} Parameters</div>", unsafe_allow_html=True)
for param in parameters[option]:
    with st.container():
        st.markdown(f'<div class="input-container"><div class="input-block">{param}</div>', unsafe_allow_html=True)
        if param == "Soil Type":
            value = st.selectbox("", list(soil_mapping.keys()), key=param)
            inputs.append(soil_mapping[value])
        elif param == "Crop Type":
            value = st.selectbox("", list(crop_mapping.keys()), key=param)
            inputs.append(crop_mapping[value])
        else:
            value = st.number_input("", key=param)
            inputs.append(value)
        st.markdown('</div>', unsafe_allow_html=True)

if st.button("Predict"):
    input_data = np.array([inputs])
    model = crop_model if option == "Crop Recommendation" else fertilizer_model
    prediction = model.predict(input_data)[0]
    
    if option == "Crop Recommendation":
        crop_mapping = {
            1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
            8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
            14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
            19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"
        }
        result = crop_mapping.get(prediction, "Unknown Crop")
    else:
        fertilizer_mapping = {
            1: "Urea", 2: "DAP", 3: "14-35-14", 4: "28-28", 5: "17-17-17", 6: "20-20", 7: "10-26-26",
        }
        result = fertilizer_mapping.get(prediction, "Unknown Fertilizer")
    
    st.markdown(f'<div class="output-block">Predicted Output: <b>{result}</b></div>', unsafe_allow_html=True)
