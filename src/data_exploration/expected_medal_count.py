import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Read the CSV file into a pandas DataFrame with specified encoding
base_dir = Path(__file__).parents[2]
programs = pd.read_csv(base_dir / './Data/summerOly_programs.csv', encoding='latin1')
athletes = pd.read_csv(base_dir / './Data/summerOly_athletes.csv')
medals = pd.read_csv(base_dir / './Data/summerOly_medal_counts.csv')

# Encode "Medal" column in athletes DataFrame
athletes.loc[athletes['Medal'] == 'No medal', 'Medal'] = 0
athletes.loc[athletes['Medal'] == 'Gold', 'Medal'] = 3
athletes.loc[athletes['Medal'] == 'Silver', 'Medal'] = 2
athletes.loc[athletes['Medal'] == 'Bronze', 'Medal'] = 1

unique_sports_from_programs = programs['Sport'].unique()
unique_sports_from_athletes = athletes['Sport'].unique()

print("----------")
print(unique_sports_from_programs)
print("---------")
print(unique_sports_from_athletes)
print("---------")

# print("----------")
# print(np.setdiff1d(unique_sports_from_athletes, unique_sports_from_programs))
# print("---------")
# print(np.setdiff1d(unique_sports_from_programs, unique_sports_from_athletes))
# print("---------")

# Create new "Discipline" column that concatenates "Sport" and "Event" and add to athletes DataFrame
# athletes['Discipline'] = athletes['Sport'] + '/' + athletes['Event']

# Drop "Sex", "Team" and "City" columns from athletes DataFrame
athletes = athletes.drop(columns=['Sex', 'Team', 'City'])

# print(athletes['Discipline'].unique())

year = 2024
