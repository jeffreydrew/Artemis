import yfinance as yf
import pandas as pd

Historical_data_path = "Historical_data/"
Backtesting_path = "Backtesting/"


# get 1 minute ticker info for aapl from 1/1/23 to 2/1/23
def get_data(symbol: str, period: str, interval: str):
    ticker = yf.Ticker(symbol)
    ticker_data = ticker.history(period=period, interval=interval)
    # keep first 5 columns
    ticker_data = ticker_data.iloc[:, :5]
    # round the prices to 3 decimal places
    ticker_data.iloc[:, :5] = ticker_data.iloc[:, :5].round(3)

    # convert to csv and save to Historical_data/aapl.csv and Backtesting/aapl.csv
    ticker_data.to_csv(f"{Historical_data_path}/{symbol}_{period}_{interval}.csv")


"""
period: data period to download (either use period parameter or use start and end) Valid periods are:
“1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”

interval: data interval (1m data is only for available for last 7 days, and data interval <1d for the last 60 days) Valid intervals are:
“1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”

start: If not using period - in the format (yyyy-mm-dd) or datetime.

end: If not using period - in the format (yyyy-mm-dd) or datetime."""

