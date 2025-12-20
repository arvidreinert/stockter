import read_data as rd
import create_data as fd
from fisims import sim
import time

class intraday_bot():
    def __init__(self,stocks_allowed):
        self.chunk = rd.data_chunk()
        self.boughts = {}
        self.lst_p = {}
        for stock in stocks_allowed:
            self.chunk.add_symbol(stock)
            self.boughts[stock] = 0
            self.lst_p[stock] = 0

    def is_bought(self,stock):
        cond = False
        if stock in self.boughts:
            if self.boughts[stock] > 0:
                cond = True
        return cond

    def signal(self,stock):
        cp = self.chunk.up_to_date_price(stock)
        while cp == 0:
            time.sleep(5)
            cp = self.chunk.up_to_date_price(stock)
        std = fd.fast_tabel(stock,dur="1d",interval="1m")
        while len(std) == 0:
            time.sleep(5)
            std = fd.fast_tabel(stock,dur="1d",interval="1m")
        cls = std["Close"][-3:]
        sma = sum(cls)/len(cls)
        ops = std["Open"][-3:]
        op1 = ops.iloc[0]
        stre = round((cp-op1)/cp*100,3)
        lb = self.lst_p[stock]
        p = round(float(cp-lb)/float(cp)*100,4)
        smadif = cp-sma
        sell = p>0.1 and lb != 0 or smadif >= 0.5
        x = sell or p <= -0.1
        z = smadif<0 and smadif>-0.5
        y = z and stre<0 and stre>-0.05
        if y and not x and self.boughts[stock] <= 10:
            self.boughts[stock] += 1
            self.lst_p[stock] = cp
            return "buy",stre
        
        elif x and self.boughts[stock] >= 1:
            return "sell",stre
        
        else:
            return "hold",cp,sma,cp-lb,stre,smadif