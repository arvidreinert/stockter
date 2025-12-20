import yfinance as yf
from datetime import datetime, timedelta

def fast_tabel(symbol,dur="5d",interval="1h"):
    ticker = yf.Ticker(symbol)
    return ticker.history(period=dur,interval=interval)

def create_data(symbol, duration={"days":60, "hours":0, "minutes":0, "seconds":0}, interval="1h", in_past={"days":0, "hours":0, "minutes":0, "seconds":0}):

    duration_delta = timedelta(days=duration["days"], hours=duration["hours"],minutes=duration["minutes"], seconds=duration["seconds"])
    
    in_past_delta = timedelta(days=in_past["days"], hours=in_past["hours"],minutes=in_past["minutes"], seconds=in_past["seconds"])

    end_date = datetime.today() - in_past_delta
    start_date = end_date - duration_delta

    start_date_yf = start_date.strftime("%Y-%m-%d")
    end_date_yf = end_date.strftime("%Y-%m-%d")
    ticker = yf.Ticker(symbol)
    h = ticker.history(start=start_date_yf, end=end_date_yf, interval=interval)
    if len(h) == 0:
        print(f"No data downloaded for {symbol} between {start_date_yf} and {end_date_yf}")
        return
    filename = f"historic_data_{symbol}.csv"
    h.to_csv(filename)