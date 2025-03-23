import eurostat
import pandas as pd
import os

# Define the dataset code and output file name
dataset_code = 'APRO_MT_PANN'
output_file = dataset_code + '_dataset.csv'

# Check if the CSV file already exists
if os.path.exists(output_file):
    print(f"{output_file} already exists. Loading from file.")
    dataset = pd.read_csv(output_file)
else:
    print(f"{output_file} not found. Fetching from Eurostat...")
    # Fetch the dataset using the Eurostat library
    dataset = eurostat.get_data_df(dataset_code)
    # Save the dataset to a CSV file
    dataset.to_csv(output_file, index=False)
    print(f"Dataset fetched and saved as {output_file}.")

# Display the first few rows of the dataset to ensure it's loaded correctly
print(dataset.head())

"""
1º step: clean data
quais as unidades de todos os valores numéricos?

get a new, curated and clean .csv file from the data
"""
# understand the data
# Print all values of the first row (index 0)
#row_index = 10
#print("Row values:")
#print(dataset.iloc[row_index].to_string())


#Understand all collumn values to convert names to better names to use template based questions

# Get all unique values in 'Column2'
# Get unique values and their counts as a dictionary for 'Column2'
#value_counts_dict_freq = dataset['freq'].value_counts().to_dict()

#print("Unique values and their counts in Column2:")
#print(value_counts_dict_freq)

"""
Determine, from the 14 questions, how many template based questions I will create and if I will create ones from chatGPT
"""

"""
If dataset is big, 100/14 = 7.14 % each template question gets from the dataset - all data needs to bse used in questions
"""

"""
create function to automate process of making .csv with "Question; ID; answer; is_impossible" for each question
"""

"""
merge all questions in .JSON like SQUAD dataset
"""