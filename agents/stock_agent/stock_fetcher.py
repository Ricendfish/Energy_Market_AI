import yfinance as yf

def get_stock(symbol="ORSTED.CO"):

    stock = yf.Ticker(symbol)
    hist = stock.history(period="1y")

    return hist.tail()

if __name__ == "__main__":
    print(get_stock())