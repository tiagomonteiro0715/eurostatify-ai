import eurostat
import pandas as pd
import os

# Define the dataset code and output file name
dataset_code = 'NASA_10_KI'
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
#print(dataset.head())


"""
1º step: clean data
quais as unidades de todos os valores numéricos?

Get a new, curated and clean .csv file from the data
"""
"""
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
"""

na_item_descriptions = {
    'B2G_B3G_RAT_S11': 'Profit Surplus Ratio for Non-Financial Corporations',
    'P51G_RAT_GDP_S1': 'Gross Value Added to GDP Ratio for Total Economy',
    'B7G_N_HAB_GR': 'Nominal Net Income per Capita Growth',
    'B7G_R_HAB_GR': 'Real Net Income per Capita Growth',
    'P51G_RAT_GDP_S1M': 'Gross Value Added to GDP Ratio for Manufacturing Sector',
    'P51G_RAT_GDP_BUS': 'Gross Value Added to GDP Ratio for Business Sector',
    'IRG_S11': 'Investment Rate Growth for Non-Financial Corporations',
    'P4_R_HAB_GR': 'Real Consumption per Capita Growth',
    'SRG_S14_S15': 'Saving Rate Growth for Households and Non-Profits',
    'IRG_S14_S15': 'Investment Rate Growth for Households and Non-Profits',
    'P51G_RAT_GDP_S13': 'Gross Value Added to GDP Ratio for Government Sector',
    'ROE_S11': 'Return on Equity for Non-Financial Corporations',
    'NFW_S14_S15': 'Net Financial Wealth for Households and Non-Profits',
    'P51G_RAT_GDP_S14': 'Gross Value Added to GDP Ratio for Households',
    'DIR_S14_S15': 'Disposable Income Ratio for Households and Non-Profits',
    'IRG_S14': 'Investment Rate Growth for Households',
    'SRG_S14': 'Saving Rate Growth for Households',
    'NFW_S14': 'Net Financial Wealth for Households',
    'DIR_S14': 'Disposable Income Ratio for Households',
    'DIR_S11': 'Disposable Income Ratio for Non-Financial Corporations',
    'ROCE_S11': 'Return on Capital Employed for Non-Financial Corporations'
}

sector_descriptions = {
    'S14_S15': 'Households and Non-Profit Institutions Serving Households',
    'S11': 'Non-Financial Corporations',
    'S14': 'Households',
    'S1': 'Total Economy (All Resident Sectors)',
    'S11_S12': 'Non-Financial and Financial Corporations',
    'S13': 'General Government'
}

country_code_map = {
    "AT": "Austria",
    "BE": "Belgium",
    "BG": "Bulgaria",
    "CY": "Cyprus",
    "CZ": "Czech Republic",
    "DE": "Germany",
    "DK": "Denmark",
    "EE": "Estonia",
    "EL": "Greece",
    "ES": "Spain",
    "FI": "Finland",
    "FR": "France",
    "HR": "Croatia",
    "HU": "Hungary",
    "IE": "Ireland",
    "IT": "Italy",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "LV": "Latvia",
    "MT": "Malta",
    "NL": "Netherlands",
    "PL": "Poland",
    "PT": "Portugal",
    "RO": "Romania",
    "SE": "Sweden",
    "SI": "Slovenia",
    "SK": "Slovakia",
    "UK": "United Kingdom",
    "CH": "Switzerland",
    "NO": "Norway",
    "IS": "Iceland",
    "RS": "Serbia",
    "TR": "Turkey",
    "AL": "Albania"
}


df = pd.read_csv('NASA_10_KI_dataset.csv')

#Understand all collumn values to convert names to better names to use template based questions

# Get all unique values in 'Column2'
# Get unique values and their counts as a dictionary for 'Column2'
value_counts_dict = dataset['geo\TIME_PERIOD'].value_counts().to_dict()

#print("Unique values and their counts in Column2:")
print(value_counts_dict)


df = df.drop(['freq', 'unit'], axis=1)
df = df[df['geo\TIME_PERIOD'] != "EA20"]
df = df[df['geo\TIME_PERIOD'] != "EU27_2020"]

df['na_item'] = df['na_item'].map(na_item_descriptions)
df['sector'] = df['sector'].map(sector_descriptions)
df['geo\TIME_PERIOD'] = df['geo\TIME_PERIOD'].map(country_code_map)

print(df)


# Specify the file path
file_path = 'NASA_10_KI_curated.csv'
# Check if the file already exists
if not os.path.exists(file_path):
    # Save the DataFrame to CSV if the file does not exist
    df.to_csv(file_path, index=False)
    print(f"DataFrame saved to {file_path}")
else:
    print(f"File already exists at {file_path}")

"""
Determine, from the 14 questions, how many template based questions I will create and if I will create ones from chatGPT
"""
"""
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
"""


# Factoid Questions: FAC
# Factoid question function
def factoid_question(na_item, sector, geo, year):
    question = f"What is the {na_item} for {sector} in {geo} in {year}?"
    # Filter data for the specific query
    result = df[(df['na_item'] == na_item) & 
                (df['sector'] == sector) & 
                (df['geo\\TIME_PERIOD'] == geo)][str(year)]
    
    # Check if result is empty
    if not result.empty:
        answer = result.values[0]
        return question, answer
    else:
        return question, None

# Additional factoid question function
def additional_factoid_question(na_item, sector, geo, year):
    question = f"What was the recorded {na_item} for {sector} in {geo} during {year}?"
    # Filter data for the specific query
    result = df[(df['na_item'] == na_item) & 
                (df['sector'] == sector) & 
                (df['geo\\TIME_PERIOD'] == geo)][str(year)]
    
    # Check if result is empty
    if not result.empty:
        answer = result.values[0]
        return question, answer
    else:
        return question, None

# Define output file path for questions
questions_file_path = 'NASA_10_KI_factoid_questions.csv'
questions = []

# Only generate questions if the file does not already exist
if not os.path.exists(questions_file_path):
    questions = []

    # Generate questions based on the template, skipping NaNs and empty results
    for index, row in df.iterrows():
        na_item = row['na_item']
        sector = row['sector']
        geo = row['geo\\TIME_PERIOD']
        
        for year in range(1950, 2024):  # Check each year from 1950 to 2023
            if not pd.isna(row[str(year)]):  # Skip if the value is NaN
                # Generate primary factoid question
                question, answer = factoid_question(na_item, sector, geo, year)
                if answer is not None:
                    question_id = f"NASA_10_KI-FAC-{geo[:2].upper()}-{year}"
                    questions.append([question, question_id, answer, "false"])
                
                # Generate additional factoid question
                question, answer = additional_factoid_question(na_item, sector, geo, year)
                if answer is not None:
                    question_id = f"NASA_10_KI-ADD-{geo[:2].upper()}-{year}"
                    questions.append([question, question_id, answer, "false"])

    # Convert the list to a DataFrame
    questions_df = pd.DataFrame(questions, columns=["Question", "ID", "Answer", "False"])

    # Save the DataFrame to CSV
    questions_df.to_csv(questions_file_path, index=False)
    print(f"Questions saved to {questions_file_path}")
else:
    print(f"The file {questions_file_path} already exists. No new questions generated.")




"""
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
"""

import pandas as pd
import os

# Load the dataset

# Define the output file path for Yes/No questions
questions_file_path = 'NASA_10_KI_yes_no_questions.csv'

# Only generate questions if the file does not already exist
if not os.path.exists(questions_file_path):
    questions = []
    threshold = 10  # Example threshold value; adjust as needed

    # Yes/No question function with threshold
    def yes_no_question(na_item, sector, geo, year, threshold):
        question = f"Was the {na_item} for {sector} in {geo} above {threshold}% in {year}?"
        result = df[(df['na_item'] == na_item) & 
                    (df['sector'] == sector) & 
                    (df['geo\\TIME_PERIOD'] == geo)][str(year)]
        
        if not result.empty:
            value = result.values[0]
            answer = "Yes" if value > threshold else "No"
            return question, answer
        else:
            return question, None

    # Additional Yes/No question function for threshold
    def additional_yes_no_question(na_item, sector, geo, year, threshold):
        question = f"Did the {na_item} for {sector} in {geo} fall below {threshold}% in {year}?"
        result = df[(df['na_item'] == na_item) & 
                    (df['sector'] == sector) & 
                    (df['geo\\TIME_PERIOD'] == geo)][str(year)]
        
        if not result.empty:
            value = result.values[0]
            answer = "Yes" if value < threshold else "No"
            return question, answer
        else:
            return question, None

    # Generate questions based on the template, skipping NaNs and empty results
    for index, row in df.iterrows():
        na_item = row['na_item']
        sector = row['sector']
        geo = row['geo\\TIME_PERIOD']
        
        for year in range(1950, 2024):  # Check each year from 1950 to 2023
            if not pd.isna(row[str(year)]):  # Skip if the value is NaN
                # Generate Yes/No question above threshold
                question, answer = yes_no_question(na_item, sector, geo, year, threshold)
                if answer is not None:
                    question_id = f"NASA_10_KI-YNO-ABOVE-{geo[:2].upper()}-{year}"
                    questions.append([question, question_id, answer, "false"])
                
                # Generate additional Yes/No question below threshold
                question, answer = additional_yes_no_question(na_item, sector, geo, year, threshold)
                if answer is not None:
                    question_id = f"NASA_10_KI-YNO-BELOW-{geo[:2].upper()}-{year}"
                    questions.append([question, question_id, answer, "false"])

    # Convert the list to a DataFrame for saving to CSV
    questions_df = pd.DataFrame(questions, columns=["Question", "ID", "Answer", "False"])
    questions_df.to_csv(questions_file_path, index=False)

    print(f"Yes/No questions saved to {questions_file_path}")
else:
    print(f"The file {questions_file_path} already exists. No new questions generated.")


"""
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
"""


# Define the output file path for Why questions
why_questions_file_path = 'NASA_10_KI_why_questions.csv'

# Only generate questions if the file does not already exist
if not os.path.exists(why_questions_file_path):
    questions = []

    # Why question function
    def why_question(na_item, sector, geo, year):
        question = f"Why did the {na_item} change in {geo} for {sector} in {year}?"
        answer = "Consider investigating macroeconomic factors, industry shifts, or policy changes that impacted these metrics during this period."
        return question, answer

    # Additional why question function
    def additional_why_question(na_item, sector, geo, year):
        question = f"What factors contributed to changes in the {na_item} for {sector} in {geo} in {year}?"
        answer = "Potential contributing factors could include inflation rates, regulatory changes, or sectoral investment shifts."
        return question, answer

    # Generate Why questions for each row and year without checking specific values
    for index, row in df.iterrows():
        na_item = row['na_item']
        sector = row['sector']
        geo = row['geo\\TIME_PERIOD']
        
        for year in range(1950, 2024):  # Create questions for each year from 1950 to 2023
            if str(year) in row and not pd.isna(row[str(year)]):  # Check for valid data in the year column
                # Generate Why question
                question, answer = why_question(na_item, sector, geo, year)
                question_id = f"NASA_10_KI-WHY-{geo[:2].upper()}-{year}"
                questions.append([question, question_id, answer, "false"])
                
                # Generate additional Why question
                question, answer = additional_why_question(na_item, sector, geo, year)
                question_id = f"NASA_10_KI-ADD-WHY-{geo[:2].upper()}-{year}"
                questions.append([question, question_id, answer, "false"])

    # Convert the list to a DataFrame for saving to CSV
    questions_df = pd.DataFrame(questions, columns=["Question", "ID", "Answer", "False"])
    questions_df.to_csv(why_questions_file_path, index=False)

    print(f"Why questions saved to {why_questions_file_path}")
else:
    print(f"The file {why_questions_file_path} already exists. No new questions generated.")



"""
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
"""


# Define the output file path for How questions
how_questions_file_path = 'NASA_10_KI_how_questions.csv'

# Only generate questions if the file does not already exist
if not os.path.exists(how_questions_file_path):
    questions = []

    # How question function
    def how_question(na_item, sector, geo, start_year, end_year):
        question = f"How did the {na_item} trend for {sector} in {geo} from {start_year} to {end_year}?"
        # Extract values for the specified range of years as columns
        year_columns = [str(year) for year in range(start_year, end_year + 1)]
        values = df[(df['na_item'] == na_item) & 
                    (df['sector'] == sector) & 
                    (df['geo\\TIME_PERIOD'] == geo)][year_columns]
        
        if not values.empty:
            trend = values.iloc[0].tolist()  # Extract row values as a list
            answer = f"The values trend from {start_year} to {end_year} as follows: {trend}"
            return question, answer
        else:
            return question, None

    # Additional how question function
    def additional_how_question(na_item, sector, geo, start_year, end_year):
        question = f"What was the pattern of change in {na_item} for {sector} in {geo} from {start_year} to {end_year}?"
        # Extract values for the specified range of years as columns
        year_columns = [str(year) for year in range(start_year, end_year + 1)]
        values = df[(df['na_item'] == na_item) & 
                    (df['sector'] == sector) & 
                    (df['geo\\TIME_PERIOD'] == geo)][year_columns]
        
        if not values.empty:
            pattern = values.iloc[0].tolist()  # Extract row values as a list
            answer = f"The change pattern from {start_year} to {end_year} shows: {pattern}"
            return question, answer
        else:
            return question, None

    # Generate How questions for each row, checking specified year ranges
    for index, row in df.iterrows():
        na_item = row['na_item']
        sector = row['sector']
        geo = row['geo\\TIME_PERIOD']
        
        # Define start and end year ranges, here we'll use every 5 years as an example
        for start_year in range(1950, 2020, 5):  # Adjust intervals as needed
            end_year = start_year + 4
            if all(str(year) in row and not pd.isna(row[str(year)]) for year in range(start_year, end_year + 1)):
                # Generate How question
                question, answer = how_question(na_item, sector, geo, start_year, end_year)
                if answer is not None:
                    question_id = f"NASA_10_KI-HOW-{geo[:2].upper()}-{start_year}-{end_year}"
                    questions.append([question, question_id, answer, "false"])
                
                # Generate additional How question
                question, answer = additional_how_question(na_item, sector, geo, start_year, end_year)
                if answer is not None:
                    question_id = f"NASA_10_KI-ADD-HOW-{geo[:2].upper()}-{start_year}-{end_year}"
                    questions.append([question, question_id, answer, "false"])

    # Convert the list to a DataFrame for saving to CSV
    questions_df = pd.DataFrame(questions, columns=["Question", "ID", "Answer", "False"])
    questions_df.to_csv(how_questions_file_path, index=False)

    print(f"How questions saved to {how_questions_file_path}")
else:
    print(f"The file {how_questions_file_path} already exists. No new questions generated.")




"""
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
"""



import pandas as pd
import os
from itertools import combinations
import random

# Define the output file path for Comparison questions
comparison_questions_file_path = 'NASA_10_KI_comparison_questions.csv'

# Only generate questions if the file does not already exist
if not os.path.exists(comparison_questions_file_path):
    # Create a dictionary for quick lookups of values by (na_item, sector, geo)
    lookup_dict = {}
    for index, row in df.iterrows():
        na_item = row['na_item']
        sector = row['sector']
        geo = row['geo\\TIME_PERIOD']
        lookup_dict[(na_item, sector, geo)] = row  # Store the row for quick year-based access

    # Comparison question functions using the lookup dictionary
    def comparison_question(na_item, sector, geo1, geo2, year):
        value1 = lookup_dict.get((na_item, sector, geo1), {}).get(str(year), None)
        value2 = lookup_dict.get((na_item, sector, geo2), {}).get(str(year), None)
        
        if pd.notna(value1) and pd.notna(value2):
            question = f"How does the {na_item} for {sector} in {geo1} compare to {geo2} in {year}?"
            answer = f"In {year}, {geo1} had a value of {value1}, while {geo2} had a value of {value2}."
            return question, answer
        return None, None

    # Adjusted settings to generate a larger number of questions
    unique_geos = df['geo\\TIME_PERIOD'].unique()
    limited_geo_pairs = random.sample(list(combinations(unique_geos, 2)), min(100, len(unique_geos) * (len(unique_geos) - 1) // 2))  # Limit to 100 pairs
    limited_years = list(range(1950, 2024, 2))  # Every 2 years from 1950 to 2023
    limited_na_sector_pairs = random.sample(list(set((na_item, sector) for (na_item, sector, _) in lookup_dict.keys())), 20)  # Limit to 20 (na_item, sector) pairs

    questions = []
    for (geo1, geo2) in limited_geo_pairs:
        for (na_item, sector) in limited_na_sector_pairs:
            for year in limited_years:
                question, answer = comparison_question(na_item, sector, geo1, geo2, year)
                if answer:
                    question_id = f"NASA_10_KI-CMP-{geo1[:2].upper()}-{geo2[:2].upper()}-{year}"
                    questions.append([question, question_id, answer, "false"])

    # Save to CSV
    questions_df = pd.DataFrame(questions, columns=["Question", "ID", "Answer", "False"])
    questions_df.to_csv(comparison_questions_file_path, index=False)
    print(f"Comparison questions saved to {comparison_questions_file_path}")
else:
    print(f"The file {comparison_questions_file_path} already exists. No new questions generated.")


"""
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
"""

# Define the output file path for List questions
list_questions_file_path = 'NASA_10_KI_list_questions.csv'

# Only generate questions if the file does not already exist
if not os.path.exists(list_questions_file_path):
    questions = []

    # List question function
    def list_question(na_item, sector, geo, year_range):
        question = f"What are the {na_item} values for {sector} in {geo} from {year_range[0]} to {year_range[1]}?"
        # Extract values for the specified range of years
        year_columns = [str(year) for year in range(year_range[0], year_range[1] + 1)]
        values = df[(df['na_item'] == na_item) & 
                    (df['sector'] == sector) & 
                    (df['geo\\TIME_PERIOD'] == geo)][year_columns]
        
        if not values.empty:
            value_list = values.iloc[0].tolist()  # Extract values as a list
            answer = f"The values from {year_range[0]} to {year_range[1]} are {value_list}"
            return question, answer
        else:
            return question, None

    # Additional list question function
    def additional_list_question(na_item, sector, geo, year_range):
        question = f"List all recorded values of {na_item} for {sector} in {geo} from {year_range[0]} to {year_range[1]}."
        # Extract values for the specified range of years
        year_columns = [str(year) for year in range(year_range[0], year_range[1] + 1)]
        values = df[(df['na_item'] == na_item) & 
                    (df['sector'] == sector) & 
                    (df['geo\\TIME_PERIOD'] == geo)][year_columns]
        
        if not values.empty:
            value_list = values.iloc[0].tolist()  # Extract values as a list
            answer = f"The recorded values are: {value_list}"
            return question, answer
        else:
            return question, None

    # Generate List questions for each row with specified year ranges
    for index, row in df.iterrows():
        na_item = row['na_item']
        sector = row['sector']
        geo = row['geo\\TIME_PERIOD']
        
        # Define year ranges, here using every 5-year range as an example
        for start_year in range(1950, 2020, 5):  # Adjust intervals as needed
            end_year = start_year + 4
            if all(str(year) in row and not pd.isna(row[str(year)]) for year in range(start_year, end_year + 1)):
                year_range = (start_year, end_year)
                
                # Generate List question
                question, answer = list_question(na_item, sector, geo, year_range)
                if answer is not None:
                    question_id = f"NASA_10_KI-LST-{geo[:2].upper()}-{start_year}-{end_year}"
                    questions.append([question, question_id, answer, "false"])
                
                # Generate additional List question
                question, answer = additional_list_question(na_item, sector, geo, year_range)
                if answer is not None:
                    question_id = f"NASA_10_KI-ADD-LST-{geo[:2].upper()}-{start_year}-{end_year}"
                    questions.append([question, question_id, answer, "false"])

    # Convert the list to a DataFrame for saving to CSV
    questions_df = pd.DataFrame(questions, columns=["Question", "ID", "Answer", "False"])
    questions_df.to_csv(list_questions_file_path, index=False)

    print(f"List questions saved to {list_questions_file_path}")
else:
    print(f"The file {list_questions_file_path} already exists. No new questions generated.")


# Remaining Question Types (WHR, WHE, WHO, QNT, MHP, OED, SBH) follow the same pattern with additional functions:
# e.g., `additional_where_question`, `additional_when_question`, etc.

"""
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
"""

# Define the output file path for QA pairs
qa_pairs_file_path = 'NASA_10_KI_what_questions.csv'

# Only generate the CSV if the file does not already exist
if not os.path.exists(qa_pairs_file_path):
    # Define the dictionary of questions and answers
    
    qa_pairs = {
    "What is the Profit Surplus Ratio for Non-Financial Corporations?": "The Profit Surplus Ratio measures the balance of primary incomes for non-financial corporations, indicating their profitability.",
    "How does Gross Value Added to GDP Ratio for the Total Economy impact economic performance?": "This ratio shows the contribution of total value added by all sectors to GDP, indicating overall economic productivity.",
    "What does Nominal Net Income per Capita Growth measure?": "It measures the growth rate of net income per person, without adjusting for inflation.",
    "Why is Real Net Income per Capita Growth important?": "It reflects income growth per person adjusted for inflation, giving a clearer picture of purchasing power.",
    "How is Gross Value Added to GDP Ratio for the Manufacturing Sector calculated?": "It is calculated by dividing the gross value added in manufacturing by GDP, showing the sector's economic contribution.",
    "What sectors are included in the Gross Value Added to GDP Ratio for the Business Sector?": "It includes all businesses in the economy, excluding government and non-profit organizations.",
    "What does Investment Rate Growth for Non-Financial Corporations indicate?": "It shows the growth rate of investments by non-financial corporations, indicating sector expansion.",
    "How does Real Consumption per Capita Growth affect living standards?": "This growth rate reflects changes in consumption adjusted for inflation, affecting the real standard of living.",
    "What is the Saving Rate Growth for Households and Non-Profits?": "This growth rate shows how savings trends change for households and non-profits, affecting capital formation.",
    "Why track Investment Rate Growth for Households and Non-Profits?": "It indicates how much households and non-profits invest, affecting future income potential.",
    "How is Gross Value Added to GDP Ratio for the Government Sector useful?": "It shows the government's contribution to GDP, reflecting the scale of government economic activity.",
    "What does Return on Equity for Non-Financial Corporations measure?": "It measures profitability as a percentage of shareholders' equity, indicating sector performance.",
    "What is Net Financial Wealth for Households and Non-Profits?": "It is the value of total assets minus liabilities, indicating overall financial stability.",
    "Why is the Gross Value Added to GDP Ratio for Households important?": "It measures households' productive contributions, relevant in analyzing personal sector productivity.",
    "How does the Disposable Income Ratio for Households and Non-Profits affect spending?": "A higher disposable income ratio usually leads to increased spending power.",
    "What does Investment Rate Growth for Households reflect?": "It reflects the rate at which households are investing, impacting economic resilience.",
    "How does Saving Rate Growth for Households affect future consumption?": "Higher savings may lead to more future consumption or financial security.",
    "Why is Net Financial Wealth for Households significant?": "It indicates financial stability and the potential for future investments or consumption.",
    "What is the Disposable Income Ratio for Households?": "It measures household income available for spending and saving after taxes.",
    "How is the Disposable Income Ratio for Non-Financial Corporations determined?": "It measures the portion of income non-financial corporations retain after taxes.",
    "What does Return on Capital Employed for Non-Financial Corporations measure?": "It shows how efficiently companies use their capital to generate profits.",
    "How does Profit Surplus Ratio for Non-Financial Corporations relate to corporate health?": "Higher ratios indicate stronger profitability and financial health.",
    "What does a rising Gross Value Added to GDP Ratio for the Total Economy signify?": "It indicates an increase in the economy's overall production and growth.",
    "Why is Nominal Net Income per Capita Growth a less accurate measure of real income?": "It doesn’t account for inflation, so real purchasing power changes aren’t shown.",
    "How does Real Net Income per Capita Growth correlate with inflation?": "By adjusting for inflation, it shows the true change in individuals' purchasing power.",
    "Why is the manufacturing sector's contribution to GDP significant?": "Manufacturing is a major contributor to employment and exports, affecting GDP.",
    "How does the business sector's GDP ratio compare to other sectors?": "It generally includes more diverse activities, reflecting broader economic conditions.",
    "What factors affect Investment Rate Growth for Non-Financial Corporations?": "Market conditions, access to finance, and corporate profits are key factors.",
    "How does Real Consumption per Capita Growth impact inflation-adjusted demand?": "Higher growth indicates increased demand without inflation, stimulating the economy.",
    "Why is Saving Rate Growth for Households important for future economic stability?": "Increased savings contribute to financial security and future spending.",
    "How does investment by households and non-profits benefit the economy?": "It stimulates economic growth through capital formation.",
    "What impact does the government’s GDP ratio have on public services?": "Higher contributions can lead to expanded public services and infrastructure.",
    "What is the significance of Return on Equity for Non-Financial Corporations?": "It is a key indicator of profitability and value creation for shareholders.",
    "How does Net Financial Wealth for Households affect spending?": "Higher net wealth can lead to increased consumer spending and investment.",
    "What is Gross Value Added to GDP Ratio?": "It’s the ratio of value added by a sector to total GDP, indicating sectoral impact.",
    "Why is the Disposable Income Ratio for Households and Non-Profits crucial?": "It reflects the capacity for households to spend and save, affecting demand.",
    "How does household investment impact long-term economic resilience?": "It provides future income potential and capital for economic growth.",
    "Why measure Saving Rate Growth for Households?": "It indicates how much of income is being saved, essential for economic stability.",
    "What does Net Financial Wealth for Households show?": "It shows the net value of household assets, indicating financial health.",
    "How does the Disposable Income Ratio for Households affect consumption?": "Higher ratios generally result in more discretionary spending.",
    "What does Return on Capital Employed indicate?": "It reflects the efficiency of capital utilization in generating profits.",
    "What affects the Profit Surplus Ratio for Corporations?": "Market demand, cost control, and operational efficiency impact profitability.",
    "How does Total Economy GDP Ratio reflect productivity?": "It shows how much value the entire economy adds, indicating economic health.",
    "What can Real Net Income per Capita Growth tell us about standard of living?": "It provides insight into income increases adjusted for cost of living changes.",
    "What drives the manufacturing sector's GDP contribution?": "Innovation, demand for exports, and industrial activity drive contributions.",
    "Why is business sector growth critical for GDP?": "It signifies broad economic health and stability, impacting employment.",
    "How do financial conditions affect Corporate Investment Rate Growth?": "Access to funding and economic confidence can encourage or hinder investment.",
    "Why is Real Consumption per Capita Growth a key economic indicator?": "It directly reflects the purchasing power and well-being of consumers.",
    "How can Household Saving Rate Growth improve economic resilience?": "Increased savings provide a buffer against economic shocks.",
    "What is the importance of Government Sector GDP Ratio?": "It reflects government activity in providing public goods and services.",
    "How does Investment Rate Growth for Households affect future financial security?": "Increased household investments can lead to improved financial security and economic stability.",
    "What does a high Disposable Income Ratio for Non-Financial Corporations indicate?": "It suggests that corporations retain a significant amount of income after taxes, potentially for reinvestment.",
    "Why measure Return on Capital Employed in the non-financial sector?": "It assesses how efficiently companies in this sector use their capital to generate returns.",
    "How does the Profit Surplus Ratio influence corporate investment?": "Higher profit ratios often lead to increased reinvestment in the business.",
    "What does the Total Economy GDP Ratio signify in terms of economic health?": "A high ratio reflects robust productivity across all sectors, indicating economic strength.",
    "Why is Real Net Income per Capita Growth a reliable indicator of wealth?": "It measures actual income gains adjusted for inflation, reflecting true improvements in wealth.",
    "How does Gross Value Added to GDP Ratio for Manufacturing impact exports?": "A high ratio indicates strong manufacturing output, which often correlates with higher export activity.",
    "What drives changes in Gross Value Added for the Business Sector?": "Productivity, labor costs, and market conditions can influence this ratio.",
    "How do economic cycles impact Investment Rate Growth for Non-Financial Corporations?": "Economic downturns can reduce investment, while expansions typically boost it.",
    "What does Real Consumption per Capita Growth indicate about household confidence?": "Higher consumption growth often signals that households feel financially secure.",
    "How does Saving Rate Growth for Households affect loan availability?": "Higher savings can lead to more deposits in banks, increasing available capital for loans.",
    "Why is tracking household and non-profit investment important?": "It provides insights into economic resilience and capital availability for long-term growth.",
    "What does a high Gross Value Added to GDP Ratio for the Government mean?": "It may indicate a substantial role of government spending in the economy.",
    "How does Return on Equity for Non-Financial Corporations affect shareholder wealth?": "Higher ROE generally means higher returns for shareholders, enhancing their wealth.",
    "How does Net Financial Wealth for Households impact financial markets?": "Greater household wealth can increase investment in financial markets, impacting asset prices.",
    "What does the Disposable Income Ratio for Households mean for consumer spending?": "A high ratio suggests households have more income to spend, fueling consumer demand.",
    "How does Household Investment Rate Growth contribute to personal wealth?": "By investing more, households increase their assets, contributing to long-term wealth.",
    "Why monitor the Savings Rate Growth in households?": "It reflects the level of financial preparedness for emergencies or future investments.",
    "What is the impact of Net Financial Wealth for Households on economic stability?": "Higher wealth contributes to financial resilience and can buffer against economic shocks.",
    "How does the Disposable Income Ratio for Corporations affect reinvestment?": "Higher ratios enable corporations to reinvest profits, fueling growth and innovation.",
    "What is the significance of a high Return on Capital Employed for Non-Financial Corporations?": "It shows that the sector is using its capital effectively to generate profits, indicating financial health.",
    "Why does Profit Surplus Ratio matter for corporate strategy?": "A high profit surplus allows corporations to explore new opportunities or expand.",
    "How does the Total Economy GDP Ratio correlate with national income?": "As this ratio grows, it generally leads to higher national income and improved standards of living.",
    "What role does inflation play in Real Net Income per Capita Growth?": "Inflation-adjusted growth provides a clearer view of income improvements and purchasing power.",
    "How does Manufacturing's GDP Ratio affect employment?": "A strong manufacturing sector often correlates with job creation, supporting economic health.",
    "What factors contribute to Gross Value Added in the Business Sector?": "Productivity, labor costs, and market conditions influence this measure."
    }


    # Convert the dictionary to a DataFrame and add ID and False columns
    qa_df = pd.DataFrame(list(qa_pairs.items()), columns=["Question", "Answer"])
    qa_df['ID'] = ["NASA_10_KI-What-" + str(index + 1).zfill(3) for index in qa_df.index]  # Generate unique IDs
    qa_df['False'] = "false"  # Set the 'False' column to 'false' for each row

    # Save the DataFrame to CSV
    qa_df.to_csv(qa_pairs_file_path, index=False)

    print(f"What pairs saved to {qa_pairs_file_path}")
else:
    print(f"The file {qa_pairs_file_path} already exists. No new file generated.")





"""
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
"""
"""
merge all questions in .JSON like SQUAD dataset
"""