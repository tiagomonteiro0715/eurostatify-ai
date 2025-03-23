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
print(dataset.head(100))



"""
1º step: clean data
"""


#Understand all collumn values to convert names to better names to use template based questions

# Get all unique values in 'Column2'
# Get unique values and their counts as a dictionary for 'Column2'
value_counts_dict_freq = dataset['freq'].value_counts().to_dict()
print("\nnique values and their counts in value_counts_dict_freq:")
print(value_counts_dict_freq)

value_counts_dict_meat = dataset['meat'].value_counts().to_dict()
print("\nUnique values and their counts in value_counts_dict_freq:")
print(value_counts_dict_meat)

value_counts_dict_meat_item = dataset['meatitem'].value_counts().to_dict()
print("\nUnique values and their counts in value_counts_dict_freq:")
print(value_counts_dict_meat_item)

value_counts_dict_unit = dataset['unit'].value_counts().to_dict()
print("\nUnique values and their counts in value_counts_dict_freq:")
print(value_counts_dict_unit)

value_counts_dict_geo = dataset['geo\TIME_PERIOD'].value_counts().to_dict()
print("\nUnique values and their counts in value_counts_dict_freq:")
print(value_counts_dict_geo)


"""
Determine, from the 14 questions, how many template based questions I will create and if I will create ones from chatGPT
"""

"""
If dataset is big, 100/14 = 7.14 % each template question gets from the dataset - all data needs to bse used in questions
"""

"""
create function to automate process of making .csv with "Dataset, Question; ID; answer; is_impossible" for each question
NOTE: dataset is used later to organize the JSON file
"""

"""
merge all questions in .JSON like SQUAD dataset
"""