from datetime import date
import pandas as pd
import urllib

start_year = 2015
current_year = date.today().year
months = ["october", "november", "december", "january", "february", "march", "april", "may", "june"]
main_df = pd.DataFrame()

for year in range(start_year, current_year + 1):
	for month in months:
		try:
			url = ("https://www.basketball-reference.com/leagues/NBA_%s_games-%s.html" % (str(year), month))
			df = pd.read_html(url)
			df = df[0]
			df = df[["Date", "Visitor/Neutral", "PTS", "Home/Neutral", "PTS.1"]]
			
			main_df = main_df.append(df, ignore_index=True)
			main_df = main_df.dropna()
			

		except urllib.error.HTTPError:
			continue
		except ValueError:
			continue

main_df.to_csv("C:\\Users\\radin\\Desktop\\Data\\data_v2.csv")