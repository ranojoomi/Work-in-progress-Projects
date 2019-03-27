import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import statsmodels.api as sm
import math
from pandas_datareader import data as web

style.use("ggplot")

choice = input("What feature would you like? (beta/value): ")


def value_10000():

    ticker = input("Enter the a ticker: ")
    time_period = input("Enter a time period (5y/3y/1y/3m/1m/ytd): ")

    df = pd.read_json("https://api.iextrading.com/1.0/stock/" + ticker + "/chart/" + time_period)
    df2 = pd.read_json("https://api.iextrading.com/1.0/stock/spy/chart/" + time_period)

    df.set_index("label", inplace=True)
    df2.set_index("label", inplace=True)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    df["value of 10000"] = (10000/df.high[0])*df["high"]
    df2["value of 10000"] = (10000/df2.high[0])*df2["high"]

    df["value of 10000"].plot(label=ticker.upper(), color="#ff9900")
    df2["value of 10000"].plot(label="SPY", color="k")

    plt.title(ticker.upper() + " Value of $10,000\n ")
    plt.xlabel(" \nDate")
    plt.ylabel("value of $10,000")
    plt.legend()

def beta_of_stock():

    ticker = input("Enter the a ticker: ")
    time_period = input("Enter a time period (5y/3y/1y/3m/1m/ytd): ")

    df = pd.read_json("https://api.iextrading.com/1.0/stock/" + ticker + "/chart/" + time_period)
    df2 = pd.read_json("https://api.iextrading.com/1.0/stock/spy/chart/" + time_period)

    df.set_index("label", inplace=True)
    df2.set_index("label", inplace=True)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    x = df2["changePercent"].tolist()
    y = df["changePercent"].tolist()

    plt.scatter(x, y, s=0.8, color="k", marker="s")

    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    model = sm.OLS(y, x).fit()
    predictions = model.predict(x)
    print(model.summary())

def risk_vs_return():

    list = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    list = list[0]
    list = list["Symbol"]

    means = []
    stdevs = []

    for symbols in list:


        goog = web.DataReader(symbols, data_source="marketwatch", start ="3/14/1970", end="3/19/2019")
        df = goog["Adj Close"]
        df2 = df.pct_change(periods=21)
        percent_list = []
        for i in range(21, len(df2), 21):

            percent_list.append(df2.iloc[i])

        mean = sum(percent_list) / len(percent_list)

        vars = []
    
        for returns in percent_list:
            vars.append((returns - mean) ** 2)

        stdev = math.sqrt(sum(vars) / (len(vars) - 1))

        means.append(mean)
        stdevs.append(stdev)

    print(stdevs)
    print(means)

if choice == "beta":
    beta_of_stock()

elif choice == "risk":
    risk_vs_return()

else:
    value_10000()

plt.show()