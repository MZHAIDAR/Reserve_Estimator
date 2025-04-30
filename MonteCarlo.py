import streamlit as st
import pandas as pd
from utils.simulations import simulate_reserves, plot_reserves
from utils.dca import calculate_eur_hyperbolic


st.set_page_config(page_title="Oil Reserves Simulation", layout="wide")
st.title("🛢️ Oil Reserves Estimator : Monte Carlo")

# Sidebar config
st.sidebar.header("📊 Simulation Settings")
N = st.sidebar.slider("Number of Simulations", 1000, 100000, 10000, 1000)
distribution = st.sidebar.radio("Distribution Type", ["Uniform", "Normal"])

st.sidebar.header("📌 Input Parameters")
inputs = {
    "area_min": st.sidebar.number_input("Area Min (acres)", min_value = 1.0 , value = 1000.0),
    "area_max": st.sidebar.number_input("Area Max (acres)", min_value = 1.0 , value = 1000.0),
    "net_pay_min": st.sidebar.number_input("Net Pay Min (ft)", min_value=1.0, value=10.0),
    "net_pay_max": st.sidebar.number_input("Net Pay Max (ft)", min_value=1.0, value=50.0),
    "porosity": st.sidebar.number_input("Porosity", min_value=0.000, max_value=1.000, value=0.250, step=0.001, format = "%.3f"),
    "water_saturation": st.sidebar.number_input("Water_Saturation", min_value=0.0, max_value=1.0, value=0.25, step=0.001, format = "%.3f"),
    "recovery": st.sidebar.number_input("Recovery Factor", min_value=0.0, max_value=1.0, value=0.3, step=0.001),
    "fvf": st.sidebar.number_input("Formation Volume Factor", min_value=1.0, max_value=3.0, value=1.2, step=0.01),
}

reserves = simulate_reserves(N, inputs, distribution)
p90, p50, p10 = reserves.quantile([0.9, 0.5, 0.1])

col1, col2 = st.columns([2, 1])
with col1:
    plot_reserves(reserves)

with col2:
    st.subheader("📌 Key Statistics")
    st.metric("P90 Reserves", f"{p90:,.2f} MMSTB")
    st.metric("P50 Reserves", f"{p50:,.2f} MMSTB")
    st.metric("P10 Reserves", f"{p10:,.2f} MMSTB")
    st.download_button("📥 Download CSV", reserves.to_csv(index=False), file_name="reserves_simulation.csv")

st.caption("Created by Zeeshan")

