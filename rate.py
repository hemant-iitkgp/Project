import pandas as pd
import os

# Read the input CSV file
input_file = "cleaned.csv"  # Replace with the name of your input file
output_file = "cleaned_output.csv"  # Replace with the desired name of your output file

data = pd.read_csv(input_file)

# Extract the first row which contains population data
population_row = data.iloc[0]

# Keep a copy of the original data for modification
processed_data = data.copy()

# Iterate over subdistrict columns to calculate rates
subdistrict_columns = [col for col in data.columns if "SubDistrict" in col]

for col in subdistrict_columns:
    population = population_row[col]  # Get the population value for the subdistrict
    processed_data[col] = (data[col] / population) * 100  # Calculate rate

# Standardize data for specific subdistricts
standardize_columns = [
    "SubDistrict-Chhanve", "SubDistrict-City", "SubDistrict-Hallia",
    "SubDistrict-Jamalpur", "SubDistrict-Kone", "SubDistrict-Lalganj",
    "SubDistrict-Manjhwan", "SubDistrict-Marihan Patehara", "SubDistrict-Naraynpur",
    "SubDistrict-Pahadi", "SubDistrict-Rajgarh", "SubDistrict-Sikhar"
]

for index, row in processed_data.iterrows():
    row_mean = row[standardize_columns].mean()
    row_std = row[standardize_columns].std()
    if row_std != 0:  # Check if standard deviation is not zero
        processed_data.loc[index, standardize_columns] = (row[standardize_columns] - row_mean) / row_std
    else:
        processed_data.loc[index, standardize_columns] = 0  # Assign 0 if standard deviation is zero

# Write the processed data into a new CSV file
processed_data.to_csv(output_file, index=False)

print(f"Processed data saved to {output_file}")