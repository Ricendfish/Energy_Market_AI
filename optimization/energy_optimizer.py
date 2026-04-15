import pandas as pd


def find_cheapest_hours(hourly_prices):

    # ensure correct columns
    df = hourly_prices.copy()

    if "price_dkk" not in df.columns:
        raise ValueError("hourly_prices must contain 'price_dkk' column")

    # sort by price
    cheapest = df.sort_values("price_dkk").head(3)

    return cheapest