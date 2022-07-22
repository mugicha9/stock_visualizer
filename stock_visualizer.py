import os
from pickle import FALSE
import matplotlib.pyplot as plt
import datetime
import pandas_datareader

stock_symbol = '^NKX'

start = datetime.datetime.fromisoformat("2022-01-01")
end = datetime.datetime.today()

data = pandas_datareader.DataReader(stock_symbol, data_source="stooq", start=start, end=end)

data.insert(0, "code", stock_symbol, allow_duplicates=False)
#data.to_csv(os.path.dirname(__file__) + "\\s_stock_data_" + stock_symbol + ".csv")
stock_close_value = data.loc[:, "Close"]
print(stock_close_value)

return_values = []
buy_values = []
average_pos = 0
position_num = 0
virtual_date = start
delta_d = datetime.timedelta(days=1)
flag = True
#Caluculate money flow
while virtual_date.date() < end.date():
    if virtual_date.day == 1:
        print("NOW: "+virtual_date.strftime("%y-%m-%d") + " ; " + end.strftime("%y-%m-%d"))
        while not (virtual_date.strftime(f"20%y-%m-%d") in data["Close"]):
            virtual_date += delta_d

        print("accept: "+virtual_date.strftime("%y-%m-%d") + " ; " + str(data["Close"][virtual_date.strftime(f"20%y-%m-%d")]))
        for i in buy_values:
            average_pos += i
        if len(buy_values) != 0:
            average_pos = average_pos / len(buy_values)
        position_num += 1
        buy_values.append(data["Close"][virtual_date.strftime(f"20%y-%m-%d")])
        return_values.append((average_pos - data["Close"][virtual_date.strftime(f"20%y-%m-%d")]) * position_num)
    virtual_date += delta_d



fig = plt.figure()

stock_fig_area = fig.add_subplot(1, 2, 1)
money_flow_area = fig.add_subplot(1, 2, 2)

stock_fig_area.plot(range(len(stock_close_value)), stock_close_value)
money_flow_area.plot(range(len(buy_values)), buy_values)

plt.show()