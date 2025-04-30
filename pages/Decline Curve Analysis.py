import streamlit as st
import matplotlib.pyplot as plt
from utils.dca import calculate_eur_hyperbolic

st.title("📉 Decline Curve Analysis (DCA)")

# User inputs
st.sidebar.header("📌 Input Parameters")
qi = st.sidebar.number_input("Initial Rate (STB/day)", min_value = 100, max_value = 2000, value=800)
Di = st.sidebar.number_input("Decline Rate (fraction/Year)", min_value=0.001, max_value=1.0, value=0.2, format="%.5f")
b = st.sidebar.number_input("b-Factor", min_value=0.0, max_value=2.0, value=0.5)
t_max_months = st.sidebar.slider("Forecast Period (Months)", 12,360, 144)

# Calculate
eur, t_vals, rates, cumulative = calculate_eur_hyperbolic(qi, Di, b, t_max_months)

# Plot
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(t_vals, rates, label="Rate (STB/day)", color = 'blue')
ax.set_ylabel("Production Rate", color = 'blue')

ax2 = ax.twinx()
ax2.plot(t_vals, cumulative,label = "Cumulative Production", color = 'green', linestyle='--')
ax2.set_ylabel("Cumulative Production (STB)", color='green')

ax.set_xlabel("Time (months)")
ax.set_title("Hyperbolic Decline Forecast")
fig.tight_layout()

lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc='center right',bbox_to_anchor=(1, 0.5))

st.pyplot(fig)

# Result
st.success(f"Estimated Ultimate Recovery (EUR): {eur:,.2f} STB")
