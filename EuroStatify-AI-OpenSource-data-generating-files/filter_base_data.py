import re
import eurostat
import pandas as pd

number_of_years = 60

# Get a list containing all Eurostat datasets metadata
datasets_list = eurostat.get_toc()

# Convert the list to a DataFrame
datasets_df = pd.DataFrame(datasets_list)

# Set the first row as the header if needed
datasets_df.columns = datasets_df.iloc[0]  # Set the first row as the header
datasets_df = datasets_df[1:]  # Remove the first row from the data

# Print the column names to confirm
print(datasets_df.columns)

# Drop the 'type' column if it exists
datasets_df = datasets_df.drop('type', axis=1, errors='ignore')
datasets_df = datasets_df.drop('last update of data', axis=1, errors='ignore')
datasets_df = datasets_df.drop('last table structure change', axis=1, errors='ignore')


# Function to extract the year from various date formats
def extract_year(date_str):
    if pd.isnull(date_str):
        return None
    match = re.search(r'\b(\d{4})\b', date_str)
    return match.group(1) if match else None

# Apply the function to 'data start' and 'data end' columns
datasets_df['data start'] = datasets_df['data start'].apply(extract_year)
datasets_df['data end'] = datasets_df['data end'].apply(extract_year)

# Convert columns to integers where applicable
datasets_df['data start'] = pd.to_numeric(datasets_df['data start'], errors='coerce')
datasets_df['data end'] = pd.to_numeric(datasets_df['data end'], errors='coerce')

# Filter rows where 'data end' is 2023 or 2024 and the interval is 20 years or more
filtered_df = datasets_df[
    (datasets_df['data end'].isin([2023, 2024])) &
    (datasets_df['data start'].notnull()) &
    ((datasets_df['data end'] - datasets_df['data start']) >= number_of_years)
]

# Display the filtered DataFrame
print("\nDatasets where 'data end' is 2023 or 2024 and the interval between 'data start' and 'data end' is " + str(number_of_years) + " years or more:")
print(filtered_df)

count_filtered_rows = len(filtered_df)

print("Number of datasets with 'data end' of 2023 or 2024 and intervals of " + str(number_of_years) + " years or more:", count_filtered_rows)

# Save the filtered DataFrame to a CSV file
output_file_path = 'filtered_datasets_' + str(number_of_years) + '_years.csv'
filtered_df.to_csv(output_file_path, index=False)