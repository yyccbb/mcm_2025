import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Read the CSV file into a pandas DataFrame with specified encoding
base_dir = Path(__file__).parents[2]
events = pd.read_csv(base_dir / './data/summerOly_programs.csv', encoding='latin1')
athletes = pd.read_csv(base_dir / './data/summerOly_athletes.csv')
medals = pd.read_csv(base_dir / './data/summerOly_medal_counts.csv')

# print(athletes.head())

year = 2024
NOCs_year = athletes[athletes['Year'] == year]['NOC'].unique()
past_3_games = (year-4, year-8, year-12)

sports = athletes['Sport'].unique()
print(sports)
# print(np.setdiff1d(disciplines, sports))
# print(np.setdiff1d(sports, disciplines))

athletes.loc[athletes['Medal'] == 'No medal', 'Medal'] = 0
athletes.loc[athletes['Medal'] == 'Gold', 'Medal'] = 3
athletes.loc[athletes['Medal'] == 'Silver', 'Medal'] = 2
athletes.loc[athletes['Medal'] == 'Bronze', 'Medal'] = 1
# print(athletes['Medal'].unique())


medal_games_NOC = []

for noc in NOCs_year:
    noc_past_3_games = athletes[(athletes['NOC'] == noc) & (athletes['Year'].isin(past_3_games))]

    for discipline in sports:
        noc_past_3_games_discipline = noc_past_3_games[noc_past_3_games['Sport'] == discipline]
        # print(noc_past_3_games_discipline.head())
        won_medals = noc_past_3_games_discipline[noc_past_3_games_discipline['Medal'] > 0]
        medals_games_in_past_3_games_discipline = len(won_medals['Year'].unique())
        won_gold_medals = noc_past_3_games_discipline[noc_past_3_games_discipline['Medal'] == 3]
        gold_medals_games_in_past_3_games_discipline = len(won_gold_medals['Year'].unique())
        won_silver_medals = noc_past_3_games_discipline[noc_past_3_games_discipline['Medal'] == 2]
        silver_medals_games_in_past_3_games_discipline = len(won_silver_medals['Year'].unique())
        medal_games_NOC.append({'NOC': noc, 'Sport': discipline, 'MedalGames': medals_games_in_past_3_games_discipline, 'GoldGames': gold_medals_games_in_past_3_games_discipline, 'SilverGames': silver_medals_games_in_past_3_games_discipline})
    # print(won_medals.head())
    medal_games_in_past_3_games = len(won_medals['Year'].unique())
    # print(medal_games_in_past_3_games)

medals_games_NOC_df = pd.DataFrame(medal_games_NOC)
print(medals_games_NOC_df.head())
# print(type(medal_games_NOC[0]))