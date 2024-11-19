import pandas as pd
from sklearn.model_selection import train_test_split
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

# Initialize the Random Forest model with reduced parameters
model = RandomForestRegressor(
    n_estimators=100,          # Reduced number of trees
    max_depth=15,              # Reduced depth
    min_samples_split=5,       # Minimum samples to split a node
    min_samples_leaf=2,        # Minimum samples at a leaf node
    max_features=0.5,          # Consider 50% of features for splits
    random_state=42
)

# Train the model
model.fit(X_train, y_train)

# Make Predictions
predictions = model.predict(X_test)

# Evaluate the Model
mse = mean_squared_error(y_test, predictions)
print(f"Mean Squared Error: {mse}")

# Save the Model with Compression
joblib.dump(model, 'model/random_forest_model.pkl', compress=3)
print("Model saved successfully!")
