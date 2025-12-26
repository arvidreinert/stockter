import read_data as rd
from datetime import datetime
import create_data as fd
from time import sleep
from random import uniform
import ast

class Sim():
    def __init__(self,cash):
        self.chunk = rd.data_chunk()
        self.stocks = {}
        self.cash = cash
        self.orders = {}
        self.last_login = ""

    def pay_dividends(self,filename):
        now = datetime.now().strftime('%Y-%m-%d')
        print(now)
        for stock in self.stocks:
            print(True)
            date,divs = self.chunk.excpected_dividends(stock)
            print(stock,date,divs)
            if date is None:
                continue
            if now != self.last_login and now == date:
                print(self.cash)
                self.cash -= divs*self.stocks[stock]["shorts"]
                self.cash += divs*self.stocks[stock]["longs"]
                print(self.cash)
        self.save_sim(filename)

    def portfolio(self):
        st = f"Portfolio   {datetime.now().strftime("%Y_%m_%d %H:%M:%S")}\n"
        st += "cash:"+str(round(self.cash,3))+"\n"
        for stock in self.stocks:
            base = f"\n{stock}  {self.stocks[stock]["amount"]}: longs: {self.stocks[stock]["longs"]}, shorts: {self.stocks[stock]["shorts"]} :"
            c = 1
            for order in self.stocks[stock]["orders"]:
                base+=f"\n  order ({c})\n\t"
                v = 0
                if order["kind"] == 0:
                    if order["is_short"]:
                        v = order["amount"]*0.05
                gain = (self.chunk.up_to_date_price(stock)-order["pwb"])*order["amount"]*order["kind"]-v
                base+=f"amount:{order["amount"]}, kind:{"long" if order["kind"] == 1 else "short" if order["kind"] == -1 else "sell"}, {"gain" if gain >= 0 else "loss"}:{gain}"
                c += 1
            st += base+"\n"
        return st
            
    def buy_order(self,symbol,amount,kind="long"):
        if not symbol in self.stocks:
            self.stocks[symbol] = {"amount":0,"longs":0,"shorts":0,"orders":[]}
        if kind == "long":
            self.stocks[symbol]["longs"] += amount
            kind = 1
        else:
            self.stocks[symbol]["shorts"] += amount
            kind = -1

        max_v,current_c = self.chunk.max_volume(symbol)
        while max_v == 0:
            sleep(5)
            max_v,current_c = self.chunk.max_volume(symbol)
        dlay = round(current_c/max_v,2)
        if dlay > 1:
            dlay = 1
        dlay = (1-dlay)*amount
        sleep(dlay)
        pri = float(self.chunk.up_to_date_price(symbol))
        while pri == -1:
            sleep(5)
            pri = float(self.chunk.up_to_date_price(symbol))
        self.stocks[symbol]["orders"].append({"amount":amount,"kind":kind,"pwb":pri})
        self.stocks[symbol]["amount"] += amount
        self.cash -= amount * pri

        return symbol+" buy order completed with "+str(dlay)+" seconds of delay; price: "+str(pri)
    
    def sell_order(self,symbol,amount,kind="long"):
        #USDT-USD 1 long
        print(symbol,amount,kind)
        max_v,current_c = self.chunk.max_volume(symbol)
        while max_v == -1:
            sleep(5)
            max_v,current_c = self.chunk.max_volume(symbol)
        dlay = round(current_c/max_v,2)
        if dlay > 1:
            dlay = 1
        dlay = (1-dlay)*amount
        kl = kind=="short"
        cond = False
        if kind == "long" and self.stocks[symbol]["longs"] >= amount:
            cond = True
        if kind == "short" and self.stocks[symbol]["shorts"] >= amount:
            cond = True
        if cond:
            if kind == "long":
                self.stocks[symbol]["longs"] -= amount
                kind = 1
            else:
                self.stocks[symbol]["shorts"] -= amount
                kind = -1
            sleep(dlay)
            pri = float(self.chunk.up_to_date_price(symbol))
            while pri == -1:
                sleep(5)
                pri = float(self.chunk.up_to_date_price(symbol))
            self.stocks[symbol]["amount"] -= amount
            self.stocks[symbol]["orders"].append({"amount":amount,"kind":0,"pwb":pri,"is_short":kl})
            if kind == 1:
                self.cash += amount * pri
            else:
                self.cash += amount * pri
                self.cash -= amount*0.05
        if self.stocks[symbol]["amount"] == 0:
            del self.stocks[symbol]
        return symbol+":sell order completed with "+str(dlay)+" seconds of delay; price: "+str(amount * pri)

    def save_sim(self,filename):
        with open(f"{filename}.txt", mode ='w')as file:
            file.write(f"stocks={self.stocks}\ncash={self.cash}\n{str(datetime.now().strftime('%Y-%m-%d'))}")

    def load_sim(self,filename):
        with open(f"{filename}.txt", mode ='r')as file:
            t = file.read().split("\n")
            self.stocks = ast.literal_eval(t[0].split("=")[1])
            self.cash = float(t[1].split("=")[1])
            self.last_login = t[2]

    def execute_bot(self,amount,symbol,order_type="hold",kind="long"):
        if order_type == "buy":
            print(symbol,amount,kind)
            return self.buy_order(symbol,amount,kind)
        if order_type == "sell":
            return self.sell_order(symbol,amount,kind)
        if order_type == "hold":
            pass