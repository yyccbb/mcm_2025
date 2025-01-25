import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a pandas DataFrame with specified encoding
events = pd.read_csv('./Data/summerOly_programs.csv', encoding='latin1')
# print(events.head())
years=events.columns.tolist()[4:]

melted_events = pd.melt(events, id_vars=['Sport', 'Discipline'], 
                        value_vars=years, 
                        var_name='Year', 
                        value_name='EventCount')
# print(melted_events.head())

events_per_sport = melted_events.groupby(['Sport','Year']).size().reset_index(name='TotalEvents')
print(events_per_sport.head())

plt.figure(figsize=(14, 8))
for sport in events_per_sport['Sport'].unique():
    sport_data = events_per_sport[events_per_sport['Sport'] == sport]
    plt.plot(sport_data['Year'], sport_data['TotalEvents'], label=sport)

plt.show()
df=pd.DataFrame(events)    
# print(df.head())
# print(df.columns.tolist()[4:])
# Display the first few rows of the DataFrame
# print(events.head())


# # Group the data by Year and Sport, and count the number of events
# events_per_year_sport = events.groupby(['Year', 'Sport']).size().reset_index(name='TotalEvents')

# # Display the grouped DataFrame
# print(events_per_year_sport.head())

# # Pivot the DataFrame to have years as rows and sports as columns
# events_pivot = events_per_year_sport.pivot(index='Year', columns='Sport', values='TotalEvents').fillna(0)

# # Display the pivoted DataFrame
# print(events_pivot.head())

# # Plot the trend of total number of events per year grouped by sport
# plt.figure(figsize=(14, 8))
# events_pivot.plot(kind='line', marker='o', ax=plt.gca())
# plt.xlabel('Year')
# plt.ylabel('Total Number of Events')
# plt.title('Trend of Total Number of Events per Year Grouped by Sport')
# plt.legend(title='Sport', bbox_to_anchor=(1.05, 1), loc='upper left')
# plt.tight_layout()  # Adjust layout to fit everything
# plt.show()
