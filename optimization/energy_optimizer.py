import pandas as pd

def find_cheapest_hours(hourly_prices, n=3):

    if "price_kwh" not in hourly_prices.columns:
        raise ValueError("hourly_prices must contain 'price_kwh' column")

    cheapest = hourly_prices.nsmallest(n, "price_kwh")

    return cheapest