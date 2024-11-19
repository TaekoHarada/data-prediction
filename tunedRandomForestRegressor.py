import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

# Load and Prepare Data
data = pd.read_csv('data/dummy_data.csv')
data['Date'] = pd.to_datetime(data['Date'])

# Extract features
data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month
data['Day'] = data['Date'].dt.day

# Use 'Category', 'Year', 'Month', 'Day', and 'IsHoliday' as features
X = pd.get_dummies(data[['Category', 'Year', 'Month', 'Day', 'IsHoliday']], drop_first=True)
y = data['Order Quantity']

# Split Data
last_year = data['Year'].max()
train_data = data[data['Year'] <= (last_year - 2)]
test_data = data[data['Year'] > (last_year - 2)]

# Prepare training and testing sets
X_train = pd.get_dummies(train_data[['Category', 'Year', 'Month', 'Day', 'IsHoliday']], drop_first=True)
y_train = train_data['Order Quantity']
X_test = pd.get_dummies(test_data[['Category', 'Year', 'Month', 'Day', 'IsHoliday']], drop_first=True)
y_test = test_data['Order Quantity']

# Set up the parameter grid
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'bootstrap': [True, False]
}

# Initialize the model
model = RandomForestRegressor(random_state=42)

# Set up GridSearchCV
grid_search = GridSearchCV(
    estimator=model,
    param_grid=param_grid,
    scoring='neg_mean_squared_error',
    cv=5,
    verbose=2,
    n_jobs=-1
)

# Fit the model to find the best parameters
grid_search.fit(X_train, y_train)

# Retrieve the best parameters
best_params = grid_search.best_params_
print("Best Parameters:", best_params)

# Train the model using the best parameters
best_model = RandomForestRegressor(
    n_estimators=best_params['n_estimators'],
    max_depth=best_params['max_depth'],
    min_samples_split=best_params['min_samples_split'],
    min_samples_leaf=best_params['min_samples_leaf'],
    bootstrap=best_params['bootstrap'],
    random_state=42
)
best_model.fit(X_train, y_train)

# Make Predictions
predictions = best_model.predict(X_test)

# Evaluate the Model
mse = mean_squared_error(y_test, predictions)
print(f"Mean Squared Error: {mse}")

# Save the Best Model
joblib.dump(best_model, 'model/random_forest_model.pkl')
print("Best model saved successfully!")