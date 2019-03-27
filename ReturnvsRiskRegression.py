import pandas as pd
from pandas_datareader import data as web
import math
import matplotlib.pyplot as plt
from matplotlib import style
from alpha_vantage.timeseries import TimeSeries
from scipy import stats
import numpy as np

style.use("ggplot")

list_of_symbols = pd.read_html("https://en.wikipedia.org/wiki/S%26P_100")

list_of_symbols = list_of_symbols[2]

list_of_symbols = list_of_symbols["Symbol"]

list_of_symbols.drop(17, inplace=True)

list_of_symbols.drop(39, inplace=True)

list_of_symbols.drop(40, inplace=True)


def get_data_as_csv():


    ts = TimeSeries(key="51FUJ8VFLTMJXYG0", output_format="pandas")
    for symbols in list_of_symbols:

        data, meta_data = ts.get_monthly_adjusted(symbol=symbols)
        percents = data.pct_change()

        print(symbols)
        print(percents.head(), "\n")

        percents.to_csv("C:\\Users\\radin\\Desktop\\Stock_Data\\"+symbols+".csv")

def calculations():

    mean_list = []
    stdev_list = []


    for symbols in list_of_symbols:

        df = pd.read_csv("C:\\Users\\radin\\Desktop\\Stock_Data\\"+symbols+".csv")

        df = df["5. adjusted close"]

        df.drop(0, inplace=True)

        mean = df.mean()*100
        stdev = df.std()*100



        mean_list.append(mean)
        stdev_list.append(stdev)



        plt.scatter(stdev, mean, s=15, c="b")

    slope, intercept, r_value, p_value, std_err = stats.linregress(stdev_list, mean_list)

    x = np.linspace(0, 20, 1000 )
    y = intercept + slope*x

    plt.plot(x, y, c="r", label="Fitted Line")
    plt.legend()
    plt.xlabel("Standard Deviation (σ)")
    plt.ylabel("Expected Return (E(X))")

    print("Slope: ", slope, " Intercept: ", intercept)
    print("R-Squared: ", r_value ** 2)



    plt.show()




def data_for_fixes(symbols):
    ts = TimeSeries(key="51FUJ8VFLTMJXYG0", output_format="pandas")
    data, meta_data = ts.get_monthly_adjusted(symbol=symbols)
    percents = data.pct_change()

    percents.to_csv("C:\\Users\\radin\\Desktop\\Stock_Data\\" + symbols + ".csv")

calculations()

