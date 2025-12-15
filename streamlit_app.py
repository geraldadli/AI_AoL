import streamlit as st
import numpy as np
import joblib

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Smart Irrigation Control",
    page_icon="🌱",
    layout="centered"
)

# -----------------------------
# Custom CSS (Pastel Farmer Theme)
# -----------------------------
st.markdown("""
<style>
/* Page background */
body {
    background-color: #f4fff4;
}
.main {
    background-color: #f4fff4;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
    color: #2e7d32;
}

/* Labels */
label {
    color: #1b5e20 !important;
    font-weight: 600;
}

/* Number input box */
.stNumberInput input {
    background-color: #e8f5e9 !important;
    color: #1b5e20 !important;   /* 👈 TEXT COLOR FIX */
    border-radius: 10px;
    border: 1px solid #a5d6a7;
}

/* Placeholder text */
.stNumberInput input::placeholder {
    color: #388e3c !important;
}

/* Button */
.stButton>button {
    background-color: #81c784;
    color: #1b5e20;
    font-weight: bold;
    border-radius: 12px;
    height: 3em;
    width: 100%;
}

/* Output card */
.output-card {
    background-color: #e8f5e9;
    padding: 20px;
    border-radius: 15px;
    margin-top: 15px;
    border-left: 6px solid #66bb6a;
    color: #1b5e20;   /* 👈 OUTPUT TEXT FIX */
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load Model
# -----------------------------
@st.cache_resource
def load_model():
    return joblib.load("DecisionTreeSmartIrrigation_1.pkl")

model = load_model()

# -----------------------------
# Title
# -----------------------------
st.markdown("## 🌱 Smart Irrigation Decision System")
st.markdown(
    "An AI-powered dashboard to control **farm actuators** "
    "based on environmental and soil nutrient data."
)

st.divider()

# -----------------------------
# Input Section
# -----------------------------
st.markdown("### 📥 Sensor Inputs")

col1, col2 = st.columns(2)

with col1:
    temperature = st.number_input("🌡 Temperature (°C)", min_value=0.0, max_value=60.0, value=30.0)
    humidity = st.number_input("💧 Humidity (%)", min_value=0.0, max_value=100.0, value=60.0)
    water_level = st.number_input("🚰 Water Level", min_value=0.0, max_value=1000.0, value=100.0)

with col2:
    N = st.number_input("🧪 Nitrogen (N)", min_value=0.0, max_value=300.0, value=255.0)
    P = st.number_input("🧪 Phosphorus (P)", min_value=0.0, max_value=300.0, value=255.0)
    K = st.number_input("🧪 Potassium (K)", min_value=0.0, max_value=300.0, value=255.0)

# -----------------------------
# Prediction
# -----------------------------
st.divider()

if st.button("🌾 Predict Actuator Status"):
    input_data = np.array([[temperature, humidity, water_level, N, P, K]])
    prediction = model.predict(input_data)[0]

    # Map output
    status_map = {0: "OFF ❌", 1: "ON ✅"}

    fan_status = status_map[prediction[0]]
    watering_plant_status = status_map[prediction[1]]
    water_pump_status = status_map[prediction[2]]

    # -----------------------------
    # Output Section
    # -----------------------------
    st.markdown("### 📤 Actuator Outputs")

    st.markdown(f"""
    <div class="output-card">
        🌬 <b>Fan Actuator:</b> {fan_status}<br><br>
        🌱 <b>Watering Plant Pump:</b> {watering_plant_status}<br><br>
        🚿 <b>Water Pump Actuator:</b> {water_pump_status}
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown(
    "<center>🌿 Built for Smart Farming • AI-powered Irrigation Control</center>",
    unsafe_allow_html=True
)
