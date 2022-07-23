import os
from pickle import FALSE
import matplotlib.pyplot as plt
import datetime
from numpy import average
import pandas, pandas_datareader

#^NKX : NIKKEI 225
# XXXX.JP : <T. XXXX>
stock_symbol = '7203.JP'

start = datetime.datetime.fromisoformat("2010-01-01")
end = datetime.datetime.fromisoformat("2022-07-20")
base_money = 30000

data = pandas_datareader.data.DataReader(stock_symbol, data_source="stooq", start=start, end=end)

data.insert(0, "code", stock_symbol, allow_duplicates=False)
#data.to_csv(os.path.dirname(__file__) + "\\s_stock_data_" + stock_symbol + ".csv")
#stock_close_value = data.loc[:, "Close"]

return_values = []
return_per = []
return_ls = []
buy_values = []
buy_dates = []
dates = []
buy_amount = []
average_values = []
average_per = []
average_pos = 0
sum_pos = 0
position_num = 0
virtual_date = start
delta_d = datetime.timedelta(days=1)
flag = True

temp_stock = 0

#Caluculate money flow
while virtual_date.date() < end.date():
    if virtual_date.day == 1:
        #print("NOW: "+virtual_date.strftime("%y-%m-%d") + " ; " + end.strftime("%y-%m-%d"))
        while not (virtual_date.strftime(f"20%y-%m-%d") in data["Close"]):
            virtual_date += delta_d
            if virtual_date.date() > end.date():
                break
        temp_stock = data["Close"][virtual_date.strftime(f"20%y-%m-%d")]
        buy_dates.append(virtual_date)
        dates.append(virtual_date)

        #print("accept: "+virtual_date.strftime("%y-%m-%d") + " ; " + str(data["Close"][virtual_date.strftime(f"20%y-%m-%d")]))
        if len(buy_values) != 0:
            average_pos = ((average_pos * sum_pos) + base_money) / (sum_pos + (base_money / temp_stock))
            average_per.append((sum(buy_values) + temp_stock) / (len(average_per) + 1))
        else:
            average_pos = temp_stock
            average_per.append(temp_stock)
            per_num = int(base_money / temp_stock)
        sum_pos += base_money / temp_stock

        buy_values.append(temp_stock)
        buy_amount.append(base_money / temp_stock)
        average_values.append(average_pos)
        return_per.append(((temp_stock - average_per[-1]) / average_per[-1]) * 100)
        return_values.append(((temp_stock - average_pos) / average_pos) * 100)
        return_ls.append(((temp_stock - buy_values[0]) / buy_values[0] ) * 100)
    else:
        while not (virtual_date.strftime(f"20%y-%m-%d") in data["Close"]):
            virtual_date += delta_d
            if virtual_date.date() > end.date():
                break
        dates.append(virtual_date)
        temp_stock = data["Close"][virtual_date.strftime(f"20%y-%m-%d")]
        return_per.append(((temp_stock - average_per[-1]) / average_per[-1]) * 100)
        return_values.append(((temp_stock - average_pos) / average_pos) * 100)
        return_ls.append(((temp_stock - buy_values[0]) / buy_values[0] ) * 100)


    virtual_date += delta_d


fig = plt.figure()

stock_fig_area = fig.add_subplot(2, 2, 1)
money_flow_area = fig.add_subplot(2, 2, 2)
return_flow_area = fig.add_subplot(2, 2, 3)
buy_amount_area = fig.add_subplot(2, 2, 4)

stock_fig_area.set_title(stock_symbol)
money_flow_area.set_title("Average Purchase Price(DCA & LS)")
return_flow_area.set_title("Return% (DCA & LS)")
buy_amount_area.set_title("Amount of Purchased Stock (DCA)")

stock_fig_area.plot(data.Close)
money_flow_area.plot(buy_dates, average_values, color='b', label="DCA")
#money_flow_area.plot(buy_dates, average_per, color='r', label="1/Month")
money_flow_area.plot(buy_dates, [buy_values[0]]*len(buy_dates), color='g', label="LS")
return_flow_area.plot(dates, return_values, color='b', label="DCA")
#return_flow_area.plot(dates, return_per, color='r', label="1/Month")
return_flow_area.plot(dates, return_ls, color='g', label="LS")
buy_amount_area.bar(range(len(buy_amount)), buy_amount)

money_flow_area.legend(loc="upper left")
return_flow_area.legend(loc="upper left")

plt.show()