import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def simulate_reserves(N, params, dist_type="Uniform"):
    def vary_net_pay(min_val, max_val):
        if dist_type == "Uniform":
            return np.random.uniform(min_val, max_val, N)
        else:
            mu = (min_val + max_val) / 2
            sigma = (max_val - min_val) / 4
            return np.clip(np.random.normal(mu, sigma, N), min_val, max_val)
    def vary_area(min_val, max_val):
        if dist_type == "Uniform":
            return np.random.uniform(min_val, max_val, N)
        else:
            mu = (min_val + max_val) / 2
            sigma = (max_val - min_val) / 4
            return np.clip(np.random.normal(mu, sigma, N), min_val, max_val)

    porosity = params['porosity']
    saturation = np.clip(1.0 - params['water_saturation'], 0.01, 1.0)
    recovery = params['recovery']
    fvf = params['fvf']

    # Variable parameter
    net_pay = vary_net_pay(params['net_pay_min'], params['net_pay_max'])
    area = vary_area(params['area_min'], params['area_max'])

    reserves = (7758 * area * net_pay * porosity * saturation * recovery / fvf)/1000000
    return pd.Series(reserves)

def plot_reserves(reserves):
    p90 = np.percentile(reserves, 10)
    p50 = np.percentile(reserves, 50)
    p10 = np.percentile(reserves, 90)

    plt.figure(figsize = (10, 7))
    plt.hist(reserves, bins =50, color = 'skyblue', edgecolor = 'black')

    plt.axvline(p90, color = 'green', linestyle = '--', linewidth = 2, label = 'P90')
    plt.axvline(p50, color = 'orange',linestyle = '--', linewidth = 2, label = 'P50')
    plt.axvline(p10, color = 'red',   linestyle = '--', linewidth = 2, label = 'P10')

    plt.xlabel("Reserves (MMSTB)")
    plt.ylabel("Frequency")
    plt.title("Reserve Distribution")
    plt.legend()
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True, linestyle = '--', alpha = 0.7)
    plt.tight_layout()
    st.pyplot(plt.gcf())
