import pandas as pd

# Load the dataset
file_path = "OriginalDataset.csv"  # Replace with your file path
df = pd.read_csv(file_path)
df = df.drop(columns=["SubDistrict-DHQ"])
# List of SubDistrict columns to check for NA values
subdistrict_columns = [
    "SubDistrict-Chhanve",
    "SubDistrict-City",
    "SubDistrict-Hallia",
    "SubDistrict-Jamalpur",
    "SubDistrict-Kone",
    "SubDistrict-Lalganj",
    "SubDistrict-Manjhwan",
    "SubDistrict-Marihan Patehara",
    "SubDistrict-Naraynpur",
    "SubDistrict-Pahadi",
    "SubDistrict-Rajgarh",
    "SubDistrict-Sikhar"
]

# Remove rows with more than 5 NA values in the specified columns
filtered_df = df[df[subdistrict_columns].isna().sum(axis=1) <= 5]

def fill_na_with_rounded_avg(row):
    for col in subdistrict_columns:
        if pd.isna(row[col]):  # Check if the cell is NA
            # Get available integer values from the column and calculate rounded average
            available_values = row[subdistrict_columns].dropna()
            rounded_avg = available_values.mean()
            row[col] = round(rounded_avg)
    return row

# Apply the function to each row
df_filled = filtered_df.apply(fill_na_with_rounded_avg, axis=1)


new_row = {
    "Indicator": "Population",  # Replace 'Column1', 'Value1' with your actual column names and values
    "S.No.": "0",
    "Parameters":"Population",
    "Type": "TOTAL",
    "SubDistrict-Chhanve":356240,
    "SubDistrict-City":600342,
    "SubDistrict-Hallia":262749,
    "SubDistrict-Jamalpur":234083,
    "SubDistrict-Kone":108887,
    "SubDistrict-Lalganj":170814,
    "SubDistrict-Manjhwan":187961,
    "SubDistrict-Marihan Patehara":24112,
    "SubDistrict-Naraynpur":266207,
    "SubDistrict-Pahadi":158277,
    "SubDistrict-Rajgarh":285521,
    "SubDistrict-Sikhar":105879
}
new_row_df = pd.DataFrame([new_row])
updated_data = pd.concat([new_row_df, df_filled], ignore_index=True)

updated_data['SubDistrict-_Mirzapur'] = updated_data[subdistrict_columns].sum(axis=1)

updated_data.to_csv("cleaned.csv", index=False)

print(f"Row added successfully to {file_path}")

