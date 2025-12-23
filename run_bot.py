from bot2 import *
import time
import traceback

symbols = ["SOL-USD","USDT-USD","DOGE-USD"]
bot = intraday_bot(symbols)
simulator = Sim(10)
counter = 0
start_time = time.perf_counter()
try:
    simulator.load_sim("bot_test2")
except:
    pass
try:
    while True:
        print(simulator.cash)
        time.sleep(5)
        print(bot.boughts)
        for symboll in symbols:
            time.sleep(1)
            sig = bot.signal(symboll)
            if len(sig) >= 5:
                print(f"{symboll}:{sig[0]},price:{sig[1]},stre:{sig[4]}%,dif to sma:{sig[-1]} or {round(float(sig[3])/float(sig[1])*100,4)}%")
            if sig[0] == "buy":
                print(simulator.execute_bot(1,symboll,sig[0]))
            if sig[0] == "sell":
                print(simulator.execute_bot(bot.boughts[symboll],symboll,"sell"))
                bot.boughts[symboll] = 0
except:
    traceback.print_exc()
    end_time = time.perf_counter()
    for symboll in symbols:
        if symboll in simulator.stocks:
            time.sleep(5)
            print("selling stock: "+symboll+str(f"  {symbols.index(symboll)}/{len(symbols)}"))
            print(simulator.execute_bot(bot.boughts[symboll],symboll,"sell"))
    print(f"stopped after {end_time - start_time} seconds. Thats {(end_time - start_time)/60} minutes")
    simulator.portfolio()
    simulator.save_sim("bot_test2")