import numpy as np

main_result = []
mean = float(input("Enter the mean: "))
std = float(input("Enter the standard deviation: "))
years = int(input("Enter your timeframe in years: "))


def simulation():

    x = np.random.normal(mean, std, years)

    starting_main = 10000
    starting = 10000
    value = []
    value.append(starting)

    for returns in x:
        starting = starting * (1 + returns)
        value.append(starting)

    if value[-1] < starting_main:
        return "Less than start"
    else:
        return "More than start"

for i in range(1000000):
    main_result.append(simulation())

wins = main_result.count("More than start")
games_played = len(main_result)

print("Success Rate is", wins / games_played)