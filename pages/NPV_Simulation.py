import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from utils.economics import simulate_npv  # <- This should be in utils/economics.py

st.title("📊 Monte Carlo NPV Simulation")

# Production input (can be replaced with actual forecast or imported from DCA)
st.markdown("### Cumulative Production Forecast (Monthly, in STB)")
cumulative = st.text_area("Enter comma-separated cumulative values", "0, 1000, 2000, 2800, 3500, 4100, 4600")
try:
    cumulative = [float(x.strip()) for x in cumulative.split(",")]
except ValueError:
    st.error("Please enter valid numbers separated by commas.")
    st.stop()

st.sidebar.header("📊 Simulation Settings")
N = st.sidebar.slider("Number of Monte Carlo Simulations", 100, 10000, 1000)

# Input Ranges

st.markdown("### Economic Parameters (Uncertainty Ranges)")
st.sidebar.header("📌 Input Parameters")
price_range = st.sidebar.slider("Oil Price Range ($/STB)", 40.0, 120.0, (60.0, 80.0))
opex_range = st.sidebar.slider("OPEX Range ($/month)", 1000.0, 15000.0, (4000.0, 9000.0))
capex_range = st.sidebar.slider("CAPEX Range ($)", 100000.0, 1500000.0, (300000.0, 800000.0))
discount_range = st.sidebar.slider("Discount Rate Range (%)", 0.0, 25.0, (8.0, 15.0))

# Run simulation
npv_results = simulate_npv(N, cumulative, price_range, opex_range, capex_range, discount_range)

# Plot
fig, ax = plt.subplots()
ax.hist(npv_results, bins=30, color="skyblue", edgecolor="black")
ax.set_title("NPV Distribution")
ax.set_xlabel("NPV ($)")
ax.set_ylabel("Frequency")

# Percentile lines
p90, p50, p10 = np.percentile(npv_results, [10, 50, 90])
for val, label, color in zip([p90, p50, p10], ['P90', 'P50', 'P10'], ['green', 'blue', 'red']):
    ax.axvline(val, linestyle="--", color=color, linewidth=2, label=f"{label}: ${val:,.0f}")
ax.legend(loc="upper left")

col1, col2 = st.columns([2, 1])
with col1:
    st.pyplot(fig)

with col2:
    st.subheader("📌 Key Statistics")
    st.metric("P90 Value", f"${p90:,.0f}")
    st.metric("P50 Value", f"${p50:,.0f}")
    st.metric("P10 Value", f"${p10:,.0f}")

