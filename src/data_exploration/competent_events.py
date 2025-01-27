import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import src.util.dataloader as dl

# Read the CSV file into a pandas DataFrame with specified encoding
events = dl.events_dataset()
athletes = dl.athletes_dataset()
medals = dl.medals_dataset()

# Discard data before 1972
athletes = athletes[athletes['Year'] >= 1972]

year = 2024
NOCs_year = athletes[athletes['Year'] == year]['NOC'].unique()
NOCS_last_game = athletes[athletes['Year'] == year-4]['NOC'].unique()
NOCS_2_games_ago = athletes[athletes['Year'] == year-8]['NOC'].unique()
NOCS_3_games_ago = athletes[athletes['Year'] == year-12]['NOC'].unique()
NOCs_in_common = np.intersect1d(NOCs_year, NOCS_last_game)
NOCs_in_common = np.intersect1d(NOCs_in_common, NOCS_2_games_ago)
NOCs_in_common = np.intersect1d(NOCs_in_common, NOCS_3_games_ago)

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

result = []
for NOC in NOCs_in_common:
    current_NOC_athletes = athletes[athletes['NOC'] == NOC]
    medal_counts_year = current_NOC_athletes[(current_NOC_athletes['Year'] == year) & (current_NOC_athletes['Medal'] > 0)]['Name'].count()
    medal_counts_past_3_games = current_NOC_athletes[(current_NOC_athletes['Year'].isin(past_3_games)) & (current_NOC_athletes['Medal'] > 0)]['Name'].count()
    result.append({'NOC': NOC, 'MedalsYear': medal_counts_year, 'MedalsPast3Games': medal_counts_past_3_games})

result_df = pd.DataFrame(result)
result_df.to_csv(dl.get_base() / './data/medal_momentum.csv')

# medal_games_NOC = []
#
# for noc in NOCs_year:
#     noc_past_3_games = athletes[(athletes['NOC'] == noc) & (athletes['Year'].isin(past_3_games))]
#
#     for discipline in sports:
#         noc_past_3_games_discipline = noc_past_3_games[noc_past_3_games['Sport'] == discipline]
#         # print(noc_past_3_games_discipline.head())
#         won_medals = noc_past_3_games_discipline[noc_past_3_games_discipline['Medal'] > 0]
#         medals_games_in_past_3_games_discipline = len(won_medals['Year'].unique())
#         won_gold_medals = noc_past_3_games_discipline[noc_past_3_games_discipline['Medal'] == 3]
#         gold_medals_games_in_past_3_games_discipline = len(won_gold_medals['Year'].unique())
#         won_silver_medals = noc_past_3_games_discipline[noc_past_3_games_discipline['Medal'] == 2]
#         silver_medals_games_in_past_3_games_discipline = len(won_silver_medals['Year'].unique())
#         medal_games_NOC.append({'NOC': noc, 'Sport': discipline, 'MedalGames': medals_games_in_past_3_games_discipline, 'GoldGames': gold_medals_games_in_past_3_games_discipline, 'SilverGames': silver_medals_games_in_past_3_games_discipline})
#     # print(won_medals.head())
#     medal_games_in_past_3_games = len(won_medals['Year'].unique())
#     # print(medal_games_in_past_3_games)
#
# medals_games_NOC_df = pd.DataFrame(medal_games_NOC)
# print(medals_games_NOC_df.head())
# print(type(medal_games_NOC[0]))


#TODO: calculate advantage sports
