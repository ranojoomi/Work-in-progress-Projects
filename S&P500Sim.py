import pandas as pd
import random
import matplotlib.pyplot as plt
from matplotlib import style
from scipy import stats

style.use("seaborn-bright")
df = pd.read_csv("C:\\Users\\radin\\Downloads\\SP500Weekly.csv")
df.set_index("Date", inplace=True)
df = df.pct_change()
df = df[["Adj Close"]]
df.drop("1950-01-02", inplace=True)
df["Close + 1"] = df["Adj Close"] + 1

mean = stats.gmean(df["Close + 1"], axis=0)
mean = mean - 1
stdev = df["Adj Close"].std()

def plotting():

    value = []
    real_values = []
    x = 0
    below = 0
    starting_amount = 10000
    value.append(starting_amount)

    while x < 52 * 10:
        returns = random.normalvariate(mean, stdev)
        starting_amount = starting_amount * (returns + 1)
        real_amount = starting_amount / ((1+0.0005686) ** x)
        real_values.append(real_amount)
        x += 1

    if real_values[(52 * 10) - 1] <= 10000:
        below += 1
        
    plt.plot(real_values)
    
    return below

y = 0
simulations_ran = 50
under_10000 = []

while y < simulations_ran:
    
    under_10000.append(plotting())
    y += 1

plt.ylabel("Value of $10,000\n ")
plt.xlabel("\n # of Weeks After Today")
plt.title("Where will the S & P 500 go in the next 10 years?")
plt.show()
