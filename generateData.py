import pandas as pd
import numpy as np
import random
from datetime import date, timedelta

def generate_date_list(start_year, end_year):
    date_list = []
    for year in range(start_year, end_year + 1):
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)
        current_date = start_date
        
        while current_date <= end_date:
            date_list.append(current_date)
            current_date += timedelta(days=1)
    
    return date_list

# Generate date list for years between 2015 and 2023
dates = generate_date_list(2015, 2023)

# List of furniture categories
furniture_categories = ["Table", "Chair", "Sofa", "Cabinet", "Bed", "Desk"]

# Create all combinations of date and furniture category
all_combinations = pd.DataFrame([(date, category) for date in dates for category in furniture_categories],
                                columns=["Date", "Category"])

# Generate random order quantities between 1 and 50
num_entries = len(all_combinations)
order_quantities = [random.randint(0, 10) for _ in range(num_entries)]
all_combinations['Order Quantity'] = order_quantities

# Add IsHoliday flag: 1 for weekends (Saturday and Sunday), 0 otherwise
all_combinations['IsHoliday'] = all_combinations['Date'].apply(
    lambda x: 1 if x.weekday() in [5, 6] else 0
)

# Weighting quantity based on the furniture category
all_combinations['Order Quantity'] = all_combinations.apply(
    lambda row: row['Order Quantity'] * 3 if row['Category'] == 'Sofa' else row['Order Quantity'],
    axis=1
)
all_combinations['Order Quantity'] = all_combinations.apply(
    lambda row: row['Order Quantity'] * 1 if row['Category'] == 'Bed' else row['Order Quantity'],
    axis=1
)
all_combinations['Order Quantity'] = all_combinations.apply(
    lambda row: row['Order Quantity'] * 0.2 if row['Category'] == 'Cabinet' else row['Order Quantity'],
    axis=1
)
all_combinations['Order Quantity'] = all_combinations.apply(
    lambda row: row['Order Quantity'] * 2.1 if row['Category'] == 'Table' else row['Order Quantity'],
    axis=1
)
all_combinations['Order Quantity'] = all_combinations.apply(
    lambda row: row['Order Quantity'] * 5 if row['Category'] == 'Chair' else row['Order Quantity'],
    axis=1
)
all_combinations['Order Quantity'] = all_combinations.apply(
    lambda row: row['Order Quantity'] * 1.25 if row['Category'] == 'Desk' else row['Order Quantity'],
    axis=1
)


# For holidays, increase the order quantity by 50%
all_combinations['Order Quantity'] = all_combinations.apply(
    lambda row: row['Order Quantity'] * 1.5 if row['IsHoliday'] == 1 else row['Order Quantity'],
    axis=1
)

# For August, increase the order quantity
all_combinations['Order Quantity'] = all_combinations.apply(
    lambda row: row['Order Quantity'] * 3 if row['Date'].month == 8 else row['Order Quantity'],
    axis=1
)

# For November, increase the order quantity of Sofa by 30%
all_combinations['Order Quantity'] = all_combinations.apply(
    lambda row: row['Order Quantity'] * 2 if row['Date'].month == 11 and row['Category'] == 'Sofa' else row['Order Quantity'],
    axis=1
)
# For December, increase the order quantity of Sofa by 30%
all_combinations['Order Quantity'] = all_combinations.apply(
    lambda row: row['Order Quantity'] * 2 if row['Date'].month == 12 and row['Category'] == 'Sofa' else row['Order Quantity'],
    axis=1
)

# For January, decrease the order quantity of Bed Sofa 50%
all_combinations['Order Quantity'] = all_combinations.apply(
    lambda row: row['Order Quantity'] * 0.2 if row['Date'].month == 1 and row['Category'] == 'Bed' else row['Order Quantity'],
    axis=1
)
# For Feb, decrease the order quantity of Bed Sofa 50%
all_combinations['Order Quantity'] = all_combinations.apply(
    lambda row: row['Order Quantity'] * 0.2 if row['Date'].month == 2 and row['Category'] == 'Bed' else row['Order Quantity'],
    axis=1
)

# Weighting quantity based on months
all_combinations['Order Quantity'] = all_combinations.apply(
    lambda row: row['Order Quantity'] * 0.1 if row['Date'].month == 1 else row['Order Quantity'],
    axis=1
)
all_combinations['Order Quantity'] = all_combinations.apply(
    lambda row: row['Order Quantity'] * 0.1 if row['Date'].month == 2 else row['Order Quantity'],
    axis=1
)
all_combinations['Order Quantity'] = all_combinations.apply(
    lambda row: row['Order Quantity'] * 0.2 if row['Date'].month == 3 else row['Order Quantity'],
    axis=1
)
all_combinations['Order Quantity'] = all_combinations.apply(
    lambda row: row['Order Quantity'] * 0.25 if row['Date'].month == 4 else row['Order Quantity'],
    axis=1
)
all_combinations['Order Quantity'] = all_combinations.apply(
    lambda row: row['Order Quantity'] * 0.3 if row['Date'].month == 5 else row['Order Quantity'],
    axis=1
)
all_combinations['Order Quantity'] = all_combinations.apply(
    lambda row: row['Order Quantity'] * 1 if row['Date'].month == 6 else row['Order Quantity'],
    axis=1
)
all_combinations['Order Quantity'] = all_combinations.apply(
    lambda row: row['Order Quantity'] * 3 if row['Date'].month == 7 else row['Order Quantity'],
    axis=1
)
all_combinations['Order Quantity'] = all_combinations.apply(
    lambda row: row['Order Quantity'] * 5 if row['Date'].month == 8 else row['Order Quantity'],
    axis=1
)
all_combinations['Order Quantity'] = all_combinations.apply(
    lambda row: row['Order Quantity'] * 3 if row['Date'].month == 9 else row['Order Quantity'],
    axis=1
)
all_combinations['Order Quantity'] = all_combinations.apply(
    lambda row: row['Order Quantity'] * 1.1 if row['Date'].month == 10 else row['Order Quantity'],
    axis=1
)
all_combinations['Order Quantity'] = all_combinations.apply(
    lambda row: row['Order Quantity'] * 1.2 if row['Date'].month == 11 else row['Order Quantity'],
    axis=1
)
all_combinations['Order Quantity'] = all_combinations.apply(
    lambda row: row['Order Quantity'] * 1.3 if row['Date'].month == 12 else row['Order Quantity'],
    axis=1
)



# Extract the year from the Date column and add (Year - 2000) to the Order Quantity
all_combinations['Date'] = pd.to_datetime(all_combinations['Date'])
all_combinations['Year'] = all_combinations['Date'].dt.year
all_combinations['Order Quantity'] += (all_combinations['Year'] - 2000)

# Check the updated DataFrame
print(all_combinations.head())

# Output the DataFrame to a CSV file
all_combinations.to_csv('data/dummy_data.csv', index=False)
