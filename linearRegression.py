# Predict the quantity of orders for the next year using linear regression
# Evaluate the performance of the linear regression model
# Take data until last year-2 as training data and data from last year-1 to last year as test data.

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np

# Load and Prepare Data
# Load your data into a pandas DataFrame
data = pd.read_csv('data/dummy_data.csv')

# Convert the date column to datetime
data['Date'] = pd.to_datetime(data['Date'])

# Extract features such as year, month, and day
data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month
data['Day'] = data['Date'].dt.day

# Use 'Category', 'Year', 'Month', and 'Day' as features
X = pd.get_dummies(data[['Category', 'Year', 'Month', 'Day']], drop_first=True)
y = data['Order Quantity']

# Split Data
# Define the last year
last_year = data['Year'].max()

# Split the data
train_data = data[data['Year'] <= (last_year - 2)]
test_data = data[data['Year'] > (last_year - 2)]

# Prepare training and testing sets
X_train = pd.get_dummies(train_data[['Category', 'Year', 'Month', 'Day', 'IsHoliday']], drop_first=True)
y_train = train_data['Order Quantity']
X_test = pd.get_dummies(test_data[['Category', 'Year', 'Month', 'Day', 'IsHoliday']], drop_first=True)
y_test = test_data['Order Quantity']

# Train the Model
model = LinearRegression()
model.fit(X_train, y_train)

# Make Predictions
predictions = model.predict(X_test)

# Evaluate the Model
mse = mean_squared_error(y_test, predictions)
print(f"Mean Squared Error: {mse}")


import joblib

# Assuming `model` is your trained LinearRegression model
joblib.dump(model, 'model/linear_regression_model.pkl')  # Save the model to a file
print("Model saved successfully!")
