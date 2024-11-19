import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import date, timedelta
import joblib

# Load the trained model
# model = joblib.load('model/linear_regression_model.pkl')
model = joblib.load('model/random_forest_model.pkl')
# model = joblib.load('model/tuned_random_forest_model.pkl')

# Specify the last year to use in the training data
last_year = 2023
this_year = last_year + 1

# Generate dates for the prediction year
start_date = date(this_year, 1, 1)
end_date = date(this_year, 12, 31)

# Create a list of all dates for the prediction year
dates_this_year = []
current_date = start_date
while current_date <= end_date:
    dates_this_year.append(current_date)
    current_date += timedelta(days=1)

# Create all combinations of date and furniture category for the prediction year
furniture_categories = ["Table", "Chair", "Sofa", "Cabinet", "Bed", "Desk"]
future_data = pd.DataFrame([(date, category) for date in dates_this_year for category in furniture_categories],
                           columns=["Date", "Category"])

# Convert Date to datetime type
future_data['Date'] = pd.to_datetime(future_data['Date'])

# Add Year, Month, Day, and IsHoliday features
future_data['Year'] = future_data['Date'].dt.year
future_data['Month'] = future_data['Date'].dt.month
future_data['Day'] = future_data['Date'].dt.day
future_data['IsHoliday'] = future_data['Date'].apply(lambda x: 1 if x.weekday() in [5, 6] else 0)

# Load your original training data
X_train = pd.read_csv('data/dummy_data.csv')

# Ensure that Date is converted to datetime and extract Year, Month, and Day
X_train['Date'] = pd.to_datetime(X_train['Date'])
X_train['Year'] = X_train['Date'].dt.year
X_train['Month'] = X_train['Date'].dt.month
X_train['Day'] = X_train['Date'].dt.day

# Filter the training data to include only records until the last year (2021)
X_train = X_train[X_train['Year'] <= last_year]

print("Number of train data", len(X_train))

# Add IsHoliday feature to the training data
X_train['IsHoliday'] = X_train['Date'].apply(lambda x: 1 if x.weekday() in [5, 6] else 0)

# Prepare the features for training and prediction
X_train = pd.get_dummies(X_train[['Category', 'Year', 'Month', 'Day', 'IsHoliday']], drop_first=True)

# Prepare the features for prediction
X_future = pd.get_dummies(future_data[['Category', 'Year', 'Month', 'Day', 'IsHoliday']], drop_first=True)

# Ensure the feature set aligns with the training data's dummy variables
X_future = X_future.reindex(columns=X_train.columns, fill_value=0)

# Make Predictions for the prediction year
future_data['PredictedOrderQuantity'] = model.predict(X_future)

# Output the predictions to a CSV file
future_data.to_csv('data/predicted_orders_this_year.csv', index=False)
print("Predictions saved to data/predicted_orders_this_year.csv")
