import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

medals= pd.read_csv('./Data/summerOly_medal_counts.csv')
medals_df=pd.DataFrame(medals)

print(medals_df.head())
#create true false dataframe of countries, boolean against year
pivot_table = medals_df.pivot_table(index='NOC', 
                                    columns='Year',
                                    values='Total', 
                                    aggfunc='count', fill_value=0)
boolean_df = pivot_table > 0
boolean_df = boolean_df.astype(int)
print(boolean_df)

boolean_df = boolean_df.reset_index()  # Reset index to include 'NOC' as a column

# Melt the DataFrame to long format
melted_df = pd.melt(boolean_df, id_vars=['NOC'], var_name='Year', value_name='Medal_Indicator')

# Pivot the DataFrame to make 'NOC' as columns and 'Year' as index
pivoted_df = melted_df.pivot(index='Year', columns='NOC', values='Medal_Indicator')

print(pivoted_df)

#Naive bayes to predict if a country's t/f probability
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

# forward analysis
X_train= boolean_df[:,-5:-3]
y_train= boolean_df[:,-2]
X_test= boolean_df[:,-4:-2]
y_test= boolean_df[:,-1]

    # Train the Naive Bayes classifier
model = GaussianNB()
model.fit(X_train, y_train)

    # Make predictions
y_pred = model.predict(X_test)

    # Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")


# # Evaluate the model
# accuracy = accuracy_score(y_test, y_pred)
# print(f"Accuracy: {accuracy * 100:.2f}%")

# #KNN to predict True False