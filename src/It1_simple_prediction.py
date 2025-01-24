import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib as plt

# Load ../Data/summerOly_medal_counts.csv as a pandas DataFrame
medals = pd.read_csv('../Data/summerOly_medal_counts.csv')

# Show basic information about the DataFrame
# print(medals.info())

# Plot medals['Total'] against medals['Year'], categorizing by medals['NOC']
nocs = medals['NOC'].unique()[:10]
print(nocs)

# plt.figure(figsize=(8, 6))
# for noc in nocs:
#     subset = medals[medals['NOC'] == noc]
#     plt.plot(subset['X'], subset['Y'], label=f'NOC {noc}')
#
# plt.xlabel('Year')
# plt.ylabel('Total Medals')
# plt.title('Total Medals per Year')
# plt.legend()
# plt.grid(True)
# plt.show()