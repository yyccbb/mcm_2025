import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib as plt

# Load ../Data/summerOly_medal_counts.csv as a pandas DataFrame
medals = pd.read_csv('../Data/summerOly_medal_counts.csv')
athletes = pd.read_csv('../data/summerOly_athletes.csv')

def first_participating_year_for_emerging_medal_winners(athletes, year=2024):
    df_year = athletes[athletes['Year'] <= year]
    df_before_year = athletes[athletes['Year'] < year]
    nocs_no_medals = df_before_year.groupby('NOC').filter(lambda group: (group['Medal'] == "No medal").all())
    nocs_no_medals_at_year = df_year.groupby('NOC').filter(lambda group: (group['Medal'] == "No medal").all())

    nocs_no_medals_at_year['Team'].unique()
    first_medals_at_year = np.setdiff1d(nocs_no_medals['Team'].unique(), nocs_no_medals_at_year['Team'].unique())

    no_medals_emerging = np.setdiff1d(nocs_no_medals_at_year['Team'].unique(), nocs_no_medals['Team'].unique())

    filtered_ds = df_year[df_year['Team'].isin(no_medals_emerging)]
    emerging_year = np.setdiff1d(df_year['Team'].unique(), df_before_year['Team'].unique())

    # Past participation records for countries that got their first medals in {year}
    NOCs_first_medal_year = df_year[df_year['Team'].isin(first_medals_at_year)]

    for noc in first_medals_at_year:
        participating_years = df_year[df_year['Team'] == noc]['Year'].unique()
        print(f"{noc} first participated in {participating_years.min()} and got their first medal in {year}")

for yr in range(2024, 1972, -4):
    print(f"\n\nYear: {yr}")
    first_participating_year_for_emerging_medal_winners(athletes, yr)
