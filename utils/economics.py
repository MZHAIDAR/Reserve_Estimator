import numpy as np

def simulate_npv(N, prod_forecast, price_range, opex_range, capex_range, discount_range):
    npvs = []
    months = np.arange(len(prod_forecast))
    monthly_prod = np.diff(np.insert(prod_forecast, 0, 0))

    for _ in range(N):
        price = np.random.uniform(*price_range)
        opex = np.random.uniform(*opex_range)
        capex = np.random.uniform(*capex_range)
        discount = np.random.uniform(*discount_range) / 100

        revenue = monthly_prod * price
        cash_flow = revenue - opex
        discount_factors = 1 / (1 + discount / 12) ** months
        discounted_cf = cash_flow * discount_factors

        npv = -capex + np.sum(discounted_cf)
        npvs.append(npv)

    return npvs
