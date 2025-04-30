import numpy as np

def hyperbolic_dca(qi, Di, b, t_months):
    t_years = t_months /12
    return qi / ((1 + b * Di * t_years) ** (1 / b))

def calculate_eur_hyperbolic(qi, Di, b, t_max_months):
    t_months = np.arange(0, t_max_months + 1)
    rates = hyperbolic_dca(qi, Di, b, t_months)
    cumulative = np.cumsum(rates)
    eur = cumulative[-1]
    return eur, t_months, rates, cumulative
