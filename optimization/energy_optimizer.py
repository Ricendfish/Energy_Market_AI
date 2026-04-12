import pandas as pd

def find_cheapest_hours(prices, hours_needed=2):

    df = pd.DataFrame({
        "hour": range(len(prices)),
        "price": prices
    })

    cheapest = df.sort_values("price").head(hours_needed)

    return cheapest


if __name__ == "__main__":

    # Example predicted hourly prices
    predicted_prices = [
        45, 42, 40, 35, 30, 25, 22, 20,
        21, 23, 27, 32, 36, 39, 41, 44,
        47, 50, 48, 46, 43, 40, 38, 36
    ]

    result = find_cheapest_hours(predicted_prices, 3)

    print("Recommended hours:")
    print(result)