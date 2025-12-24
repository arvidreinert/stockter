import csv
import create_data
import yfinance as yf

class data_chunk():
    def __init__(self):
        self.symbols = {}

    def add_symbol(self,symbol):
        self.symbols[symbol] = {"datetimes":[], 'closes':[], 'highs':[], 'lows':[], 'opens':[], 'volumes':[]}

    def prepare_data(self,symbol):
        with open(f"historic_data_{symbol}.csv", mode ='r')as file:
            content = csv.reader(file)
            x = 0
            row = []
            for line in content:
                if x == 0:
                    row = line
                else:
                    self.symbols[symbol]["datetimes"].append(line[0])
                    self.symbols[symbol]["closes"].append(float(line[row.index("Close")]))
                    self.symbols[symbol]["highs"].append(float(line[row.index("High")]))
                    self.symbols[symbol]["lows"].append(float(line[row.index("Low")]))
                    self.symbols[symbol]["opens"].append(float(line[row.index("Open")]))
                    self.symbols[symbol]["volumes"].append(float(line[row.index("Volume")]))
                x += 1

    def sma(self,symbol,statistic="closes"):
        if statistic in list(self.symbols[symbol]) and not statistic == "datetimes":
            return sum(self.symbols[symbol][statistic])/len(self.symbols[symbol][statistic])
        else:
            return "error:symbol or statistic not found"
        
    def max_volume(self,symbol):
        print(symbol)
        h = create_data.fast_tabel(symbol)
        if h.empty:
            return -1,-1
        h = h["Volume"]

        return max(h),h.iloc[-1]
    
    def get_data(self,symbol,statistic):
        if statistic in list(self.symbols[symbol]):
            return self.symbols[symbol][statistic]
        else:
            return "error:symbol or statistic not found"

    def get_all_data(self,symbol):
        return self.symbols[symbol]
    
    def up_to_date_price(self,symbol):
        return self.__search_comp(symbol)
    
    def excpected_dividends(self,symbol):
        return self.__get_dividends(symbol)
    
    def __search_comp(self,ticker_symbol):
        ticker = yf.Ticker(ticker_symbol)
        try:
            current_price = ticker.history(period="1d")['Close'].iloc[-1]
        except:
            current_price = -1
        return current_price

    def __get_dividends(self,ticker_symbol):
        ticker = yf.Ticker(ticker_symbol)
        if ticker.dividends.empty:
            return None, 0
        date = ticker.dividends.index[-1]
        div_amount = ticker.dividends.iloc[-1]
        return date.strftime('%Y-%m-%d'),div_amount
