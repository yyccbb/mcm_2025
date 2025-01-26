import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import src.util.dataloader as dl

# Load dataset
data = dl.train_dataset()

# Train-test split
train_data = data[data['Year'] < 2024].reset_index(drop=True)
test_data = data[data['Year'] == 2024].reset_index(drop=True)

# Reformat dataset into a timeseries dataset, where the Year column is used as the timeseries index
train_data = train_data.sort_values(by='Year', ascending=False).reset_index(drop=True)
train_data = train_data.drop(columns=['Year'])
test_data = test_data.drop(columns=['Year'])

# One-hot encode the 'Country' column
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
train_data_encoded = pd.DataFrame(encoder.fit_transform(train_data[['Country']]))
train_data_encoded.columns = encoder.get_feature_names_out(['Country'])
train_data = pd.concat([train_data_encoded, train_data.drop(columns=['Country'])], axis=1)
# print(train_data.head())

pd.set_option('display.max_columns', 10)
test_data_encoded = pd.DataFrame(encoder.transform(test_data[['Country']]))
test_data_encoded.columns = encoder.get_feature_names_out(['Country'])
test_data = pd.concat([test_data_encoded, test_data.drop(columns=['Country'])], axis=1)

# test_data.to_csv('lstm_test.csv', sep=',', index=True)

# Isolate the labels
y_train_total = train_data['#Total Medals']
y_train_gold = train_data['#Gold']
X_train = train_data.drop(columns=['#Gold', '#Total Medals'])

# X_train.to_csv('lstm_train.csv', sep=',', index=True)

y_test_total = test_data['#Total Medals']
y_test_gold = test_data['#Gold']
X_test = test_data.drop(columns=['#Gold', '#Total Medals'])

# Standardize the features
#TODO
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Check for NaN values
# print(X_train.shape)
# print(X_test.shape)
assert (X_train.isna().sum()).sum() == 0

# Transform the data for LSTM
# Reshape the data into 3D arrays
timesteps = 2
X_train_reshaped = X_train_scaled.reshape((int(X_train_scaled.shape[0] / timesteps), timesteps, X_train_scaled.shape[1]), order='F')
X_test_reshaped = X_test_scaled.reshape((X_test_scaled.shape[0], 1, X_test_scaled.shape[1]), order='F')

y_train_gold_reshaped = y_train_gold.values.reshape((int(y_train_gold.shape[0] / timesteps), timesteps), order='F')
y_train_total_reshaped = y_train_total.values.reshape((int(y_train_total.shape[0] / timesteps), timesteps), order='F')
print(y_train_gold_reshaped.shape)


# Define the model

model_gold = tf.keras.models.Sequential([
    tf.keras.Input(shape=(X_train_reshaped.shape[1], X_train_reshaped.shape[2])),
    tf.keras.layers.LSTM(64, return_sequences=True),
    tf.keras.layers.LSTM(64, return_sequences=False),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1, activation='linear')
])

model_gold.compile(optimizer='adam', loss='mse')

# model_gold.summary()

model_total = tf.keras.models.Sequential([
    tf.keras.Input(shape=(X_train_reshaped.shape[1], X_train_reshaped.shape[2])),
    tf.keras.layers.LSTM(64, return_sequences=True),
    tf.keras.layers.LSTM(64, return_sequences=False),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1, activation='linear')
])

model_total.compile(optimizer='adam', loss='mse')

# Train the model
model_gold.fit(X_train_reshaped, y_train_gold_reshaped, epochs=100, batch_size=1, verbose=1)
model_total.fit(X_train_reshaped, y_train_total_reshaped, epochs=100, batch_size=1, verbose=1)

# Evaluate the model
y_test_gold_reshaped = y_test_gold.values.reshape((y_test_gold.shape[0], 1), order='F')
y_pred_gold = model_gold.predict(X_test_reshaped)
y_test_total_reshaped = y_test_total.values.reshape((y_test_total.shape[0], 1), order='F')
y_pred_total = model_total.predict(X_test_reshaped)

print("\nGold Medals Prediction (2024 Test Data):")
print("Mean Squared Error (MSE):", mean_squared_error(y_test_gold_reshaped, y_pred_gold))
print("R-squared (R2):", r2_score(y_test_gold_reshaped, y_pred_gold))

print("\nTotal Medals Prediction (2024 Test Data):")
print("Mean Squared Error (MSE):", mean_squared_error(y_test_total_reshaped, y_pred_total))
print("R-squared (R2):", r2_score(y_test_total_reshaped, y_pred_total))
