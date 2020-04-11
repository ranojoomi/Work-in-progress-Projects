import math
import matplotlib.pyplot as plt
import pandas_datareader as web
import pandas as pd
import datetime as dt
from matplotlib.pyplot import style

style.use("ggplot")
start = dt.datetime(1970, 1, 1)
end = dt.datetime.now()

USA = "^GSPC"
Canada = "^GSPTSE"
Japan = "^N225"

def MAIN():

    data = web.get_data_yahoo(USA, start, end)[["Close"]]
    data = data.rename(columns={"Close":"S&P 500"})
    data_2 = web.get_data_yahoo(Canada, start, end)[["Close"]]
    data_2 = data_2.rename(columns={"Close":"TSX 60"})
    data_3 = web.get_data_yahoo(Japan, start, end)[["Close"]]
    data_3 = data_3.rename(columns={"Close":"Nikkei 225"})

    frames = [data, data_2, data_3]
    result = pd.concat(frames, axis=1)
    result.dropna(inplace=True)

    index = pd.DataFrame(index=result.index)

    SP_List = []
    TSX_List = []
    Nikkei_List = []
    seven_list = []

    for i in range(len(result)):
        indexed = (100 / result["S&P 500"][0])*result["S&P 500"][i]
        SP_List.append(indexed)
        indexed = (100 / result["TSX 60"][0])*result["TSX 60"][i]
        TSX_List.append(indexed)
        indexed = (100 / result["Nikkei 225"][0])*result["Nikkei 225"][i]
        Nikkei_List.append(indexed)
        indexed = (100 * ((1 + 0.00026852275) ** i))
        seven_list.append(indexed)

    index["S&P 500 index"] = SP_List
    index["TSX index"] = TSX_List
    index["Nikkei 225 index"] = Nikkei_List
    index["7%"] = seven_list

    index_log = pd.DataFrame(index=result.index)

    SP_List_Log = []
    TSX_List_Log = []
    Nikkei_List_Log = []
    seven_list_Log = []

    for i in range(len(result)):
        SP_List_Log.append(math.log(index["S&P 500 index"][i]))
        TSX_List_Log.append(math.log(index["TSX index"][i]))
        Nikkei_List_Log.append(math.log(index["Nikkei 225 index"][i]))
        seven_list_Log.append(math.log(index["7%"][i]))

    index_log["S&P 500"] = SP_List_Log
    index_log["S&P/TSX 60"] = TSX_List_Log
    index_log["Nikkei 225 "] = Nikkei_List_Log
    index_log["Consistent 7% Return"] = seven_list_Log

    my_colors = ['b', 'r', 'g', 'k']
    my_linetype = ["solid", "solid", "solid", "dashed"]
    fig, ax = plt.subplots()
    for col, color, linetype in zip(index_log.columns, my_colors, my_linetype):
        index_log[col].plot(color=color, linestyle=linetype, ax=ax)
    plt.ylabel("Natural Log of Index", labelpad=20)
    plt.xlabel("Years", labelpad=20)
    plt.legend(loc="upper left")
    plt.show()

MAIN()