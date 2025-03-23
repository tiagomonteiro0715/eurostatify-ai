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


"""
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
"""


df = pd.read_csv('IRT_LT_MCBY_A_dataset.csv')

df = df.drop(columns=['freq', 'int_rt'])

# Dictionary mapping of country codes to full country names
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
    "EA": "Euro Area",
}

# Replace country codes with full country names in the "geo" column
df = df[df['geo\TIME_PERIOD'] != "EU27_2020"]
df['geo\TIME_PERIOD'] = df['geo\TIME_PERIOD'].map(country_code_map)
print(df)


# Specify the file path
file_path = 'IRT_LT_MCBY_A_curated.csv'
# Check if the file already exists
if not os.path.exists(file_path):
    # Save the DataFrame to CSV if the file does not exist
    df.to_csv(file_path, index=False)
    print(f"DataFrame saved to {file_path}")
else:
    print(f"File already exists at {file_path}")

"""
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
"""

# Factoid Questions: **FAC**
def get_interest_rate_for_year_country(year: int, country: str) -> tuple:
    """
    Returns the interest rate for a specific country and year as separate question and answer strings.
    """
    question = f"What was the interest rate in {country} in {year}?"
    # Implement data lookup logic here
    answer = f"The interest rate in {country} in {year} was X%."
    return question, answer



from datetime import datetime

# Define today's date for the question IDs
today_date = datetime.now().strftime("%d/%m/%Y")

# List of countries and years in the dataset
countries = df['geo\\TIME_PERIOD'].dropna().unique()  # Ensure no NaN values in the countries list
years = df.columns[1:]  # Exclude the 'geo\TIME_PERIOD' column to get the years

# Helper function to format the question ID
def generate_id(question_type, country_code, date, index):
    return f"IRT_LT_MCBY_A-{question_type}-{country_code}-{date}-{index:02d}"

# Lists to store generated question data
questions = []
ids = []
answers = []
falses = []

# Generate questions and answers only if data is available
index = 1
for country in countries:
    # Generate the 2-letter code from the country name
    country_code = ''.join([word[0] for word in country.split()]).upper()

    # Loop over each year
    for year in years:
        # Get interest rate data for the country and year
        interest_rate = df[df['geo\\TIME_PERIOD'] == country][year].values[0]
        
        # Only proceed if the interest rate is not NaN
        if pd.notna(interest_rate):
            # Generate questions and answers for each factoid function
            # 1st question: Interest rate in a specific year
            question1, answer1 = get_interest_rate_for_year_country(int(year), country)
            questions.append(question1)
            ids.append(generate_id("FAC", country_code, today_date, index))
            answers.append(f"The interest rate in {country} in {year} was {interest_rate}%.")
            falses.append("False")
            index += 1

# Create the new DataFrame
questions_df = pd.DataFrame({
    "Question": questions,
    "ID": ids,
    "Answer": answers,
    "False": falses
})

# Save to CSV
questions_df.to_csv('IRT_LT_MCBY_A_factual_questions.csv', index=False)
print("Questions saved to IRT_LT_MCBY_A_questions.csv")

"""
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
"""


# Yes/No Questions: **YNO**
def has_negative_interest_rate_in_year(year: int, country: str) -> tuple:
    """
    Checks if the interest rate was negative for a given country and year.
    """
    question = f"Was the interest rate negative in {country} in {year}?"
    # Implement data lookup logic here
    answer = "Yes" if True else "No"  # replace with actual condition
    return question, answer

def was_interest_rate_above_threshold(year: int, country: str, threshold: float) -> tuple:
    """
    Checks if the interest rate was above a threshold in a specific year for a country.
    """
    question = f"Was the interest rate above {threshold}% in {country} in {year}?"
    # Implement data lookup logic here
    answer = "Yes" if True else "No"  # replace with actual condition
    return question, answer

import pandas as pd
from datetime import datetime

# Load the cleaned data
df = pd.read_csv('IRT_LT_MCBY_A_curated.csv')  

# Define today's date for the question IDs
today_date = datetime.now().strftime("%d/%m/%Y")

# List of countries and years in the dataset
countries = df['geo\\TIME_PERIOD'].dropna().unique()  # Ensure no NaN values in the countries list
years = df.columns[1:]  # Exclude the 'geo\TIME_PERIOD' column to get the years

# Helper function to format the question ID
def generate_id(question_type, country_code, date, index):
    return f"IRT_LT_MCBY_A-{question_type}-{country_code}-{date}-{index:02d}"

# Lists to store generated question data
questions = []
ids = []
answers = []
falses = []

# Threshold value for question generation
threshold = 5.0

# Generate Yes/No questions only if data is available
index = 1
for country in countries:
    # Generate the 2-letter code from the country name
    country_code = ''.join([word[0] for word in country.split()]).upper()

    # Loop over each year
    for year in years:
        # Get interest rate data for the country and year
        interest_rate = df[df['geo\\TIME_PERIOD'] == country][year].values[0]
        
        # Only proceed if the interest rate is not NaN
        if pd.notna(interest_rate):
            # 1st question: Was the interest rate negative?
            question1 = f"Was the interest rate negative in {country} in {year}?"
            actual_answer1 = "Yes" if interest_rate < 0 else "No"
            questions.append(question1)
            ids.append(generate_id("YNO", country_code, today_date, index))
            answers.append(actual_answer1)
            falses.append("False")
            index += 1

            # 2nd question: Was the interest rate above a certain threshold?
            question2 = f"Was the interest rate above {threshold}% in {country} in {year}?"
            actual_answer2 = "Yes" if interest_rate > threshold else "No"
            questions.append(question2)
            ids.append(generate_id("YNO", country_code, today_date, index))
            answers.append(actual_answer2)
            falses.append("False")
            index += 1

# Create the new DataFrame
questions_df = pd.DataFrame({
    "Question": questions,
    "ID": ids,
    "Answer": answers,
    "False": falses
})

# Save to CSV
questions_df.to_csv('IRT_LT_MCBY_A_yes_no_questions.csv', index=False)
print("Yes/No questions saved to IRT_LT_MCBY_A_yes_no_questions.csv")

"""
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
"""

# Why Questions: **WHY**
def reason_for_interest_rate_decline(country: str, start_year: int, end_year: int) -> tuple:
    """
    Provides reasons for a decline in interest rates over a time period.
    """
    question = f"Why did the interest rate decline in {country} between {start_year} and {end_year}?"
    answer = "Possible reasons could include economic policies, market conditions, or inflation control efforts."
    return question, answer

def why_interest_rate_increased_in_year(year: int, country: str) -> tuple:
    """
    Gives reasons for an increase in interest rates in a specific year.
    """
    question = f"Why did the interest rate increase in {country} in {year}?"
    answer = "Interest rate increases may be due to high inflation, central bank policies, or economic growth."
    return question, answer

import pandas as pd
from datetime import datetime

# Load the cleaned data
df = pd.read_csv('IRT_LT_MCBY_A_curated.csv')  

# Define today's date for the question IDs
today_date = datetime.now().strftime("%d/%m/%Y")

# List of countries and years in the dataset
countries = df['geo\\TIME_PERIOD'].dropna().unique()  # Ensure no NaN values in the countries list
years = [int(y) for y in df.columns[1:]]  # Convert years to integers for easier comparison

# Helper function to format the question ID
def generate_id(question_type, country_code, date, index):
    return f"IRT_LT_MCBY_A-{question_type}-{country_code}-{date}-{index:02d}"

# Lists to store generated question data
questions = []
ids = []
answers = []
falses = []

# Generate Why questions only if data shows a rise or decline
index = 1
for country in countries:
    # Generate the 2-letter code from the country name
    country_code = ''.join([word[0] for word in country.split()]).upper()
    
    # Loop over each year to detect increases or declines in interest rates
    for i in range(1, len(years)):
        current_year = years[i]
        previous_year = years[i - 1]
        
        # Get interest rates for the country in consecutive years
        interest_rate_current = df.loc[df['geo\\TIME_PERIOD'] == country, str(current_year)].values[0]
        interest_rate_previous = df.loc[df['geo\\TIME_PERIOD'] == country, str(previous_year)].values[0]
        
        # Only proceed if both interest rates are available
        if pd.notna(interest_rate_current) and pd.notna(interest_rate_previous):
            # Check if there was a decline
            if interest_rate_current < interest_rate_previous:
                question1 = f"Why did the interest rate decline in {country} between {previous_year} and {current_year}?"
                answer1 = "Possible reasons could include economic policies, market conditions, or inflation control efforts."
                questions.append(question1)
                ids.append(generate_id("WHY", country_code, today_date, index))
                answers.append(answer1)
                falses.append("False")
                index += 1
            
            # Check if there was an increase
            elif interest_rate_current > interest_rate_previous:
                question2 = f"Why did the interest rate increase in {country} in {current_year}?"
                answer2 = "Interest rate increases may be due to high inflation, central bank policies, or economic growth."
                questions.append(question2)
                ids.append(generate_id("WHY", country_code, today_date, index))
                answers.append(answer2)
                falses.append("False")
                index += 1

# Create the new DataFrame
questions_df = pd.DataFrame({
    "Question": questions,
    "ID": ids,
    "Answer": answers,
    "False": falses
})

# Save to CSV
questions_df.to_csv('IRT_LT_MCBY_A_why_questions.csv', index=False)
print("Why questions saved to IRT_LT_MCBY_A_why_questions.csv")

"""
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
"""


# How Questions: **HOW**
def calculate_average_interest_rate(country: str, start_year: int, end_year: int) -> tuple:
    """
    Calculates the average interest rate over a time period.
    """
    question = f"How can I calculate the average interest rate in {country} from {start_year} to {end_year}?"
    # Calculate average logic here
    answer = "The average interest rate in {country} from {start_year} to {end_year} is X%."
    return question, answer

def how_interest_rate_impacts_economy(country: str) -> tuple:
    """
    Explains the impact of interest rate on the economy.
    """
    question = f"How does the interest rate impact the economy of {country}?"
    answer = "Interest rates impact borrowing costs, consumer spending, and economic growth."
    return question, answer

import pandas as pd
from datetime import datetime

# Load the cleaned data
df = pd.read_csv('IRT_LT_MCBY_A_curated.csv')  

# Define today's date for the question IDs
today_date = datetime.now().strftime("%d/%m/%Y")

# List of countries and years in the dataset
countries = df['geo\\TIME_PERIOD'].dropna().unique()  # Ensure no NaN values in the countries list
years = [int(y) for y in df.columns[1:]]  # Convert years to integers for easier range selection

# Helper function to format the question ID
def generate_id(question_type, country_code, date, index):
    return f"IRT_LT_MCBY_A-{question_type}-{country_code}-{date}-{index:02d}"

# Lists to store generated question data
questions = []
ids = []
answers = []
falses = []

# Generate How questions only if data is available
index = 1
for country in countries:
    # Generate the 2-letter code from the country name
    country_code = ''.join([word[0] for word in country.split()]).upper()
    
    # Loop over different periods to calculate averages
    for start_idx in range(len(years) - 5):  # Adjust range for multi-year windows
        start_year = years[start_idx]
        end_year = years[start_idx + 5]
        
        # Get interest rate data for the country in the specified period
        interest_rates = df.loc[df['geo\\TIME_PERIOD'] == country, df.columns[1+start_idx:1+start_idx+6]].values[0]
        
        # Only proceed if all interest rates in the period are available (no NaNs)
        if pd.notna(interest_rates).all():
            # Calculate average interest rate over the period
            avg_interest_rate = round(interest_rates.mean(), 2)
            
            # Generate question for calculating average interest rate over time
            question1 = f"What is the average interest rate in {country} from {start_year} to {end_year}?"
            answer1 = f"The average interest rate in {country} from {start_year} to {end_year} is {avg_interest_rate}%."
            questions.append(question1)
            ids.append(generate_id("HOW", country_code, today_date, index))
            answers.append(answer1)
            falses.append("False")
            index += 1

    # Generate question on how interest rates impact the economy
    question2 = f"How does the interest rate impact the economy of {country}?"
    answer2 = "Interest rates impact borrowing costs, consumer spending, and economic growth."
    questions.append(question2)
    ids.append(generate_id("HOW", country_code, today_date, index))
    answers.append(answer2)
    falses.append("False")
    index += 1

# Create the new DataFrame
questions_df = pd.DataFrame({
    "Question": questions,
    "ID": ids,
    "Answer": answers,
    "False": falses
})

# Save to CSV
questions_df.to_csv('IRT_LT_MCBY_A_how_questions.csv', index=False)
print("How questions saved to IRT_LT_MCBY_A_how_questions.csv")

"""
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
"""


# Comparison Questions: **CMP**
def compare_interest_rates_between_countries(country1: str, country2: str, year: int) -> tuple:
    """
    Compares interest rates for two countries in a specific year.
    """
    question = f"How do the interest rates compare between {country1} and {country2} in {year}?"
    # Logic to compare interest rates
    answer = f"In {year}, the interest rate in {country1} was X% and in {country2} was Y%."
    return question, answer

def compare_interest_rate_change(country: str, year1: int, year2: int) -> tuple:
    """
    Compares the interest rate between two years for a country.
    """
    question = f"How did the interest rate change in {country} from {year1} to {year2}?"
    # Logic for difference
    answer = f"The interest rate in {country} changed by Z% between {year1} and {year2}."
    return question, answer

import pandas as pd
from datetime import datetime

# Load the cleaned data
df = pd.read_csv('IRT_LT_MCBY_A_curated.csv')  

# Define today's date for the question IDs
today_date = datetime.now().strftime("%d/%m/%Y")

# List of countries and years in the dataset
countries = df['geo\\TIME_PERIOD'].dropna().unique()  # Ensure no NaN values in the countries list
years = [int(y) for y in df.columns[1:]]  # Convert years to integers for easier comparison

# Helper function to format the question ID
def generate_id(question_type, country_codes, date, index):
    return f"IRT_LT_MCBY_A-{question_type}-{country_codes}-{date}-{index:02d}"

# Lists to store generated question data
questions = []
ids = []
answers = []
falses = []

# Generate Comparison questions only if data is available
index = 1
for i, country1 in enumerate(countries):
    # Generate the 2-letter code from the first country name
    country_code1 = ''.join([word[0] for word in country1.split()]).upper()
    
    # Loop over subsequent countries to compare with country1
    for j, country2 in enumerate(countries[i+1:], start=i+1):
        country_code2 = ''.join([word[0] for word in country2.split()]).upper()
        combined_country_code = ''.join(sorted([country_code1, country_code2]))

        # Loop over each year to compare interest rates
        for year in years:
            # Get interest rates for both countries in the same year
            interest_rate1 = df.loc[df['geo\\TIME_PERIOD'] == country1, str(year)].values[0]
            interest_rate2 = df.loc[df['geo\\TIME_PERIOD'] == country2, str(year)].values[0]

            # Only proceed if both interest rates are available
            if pd.notna(interest_rate1) and pd.notna(interest_rate2):
                question1 = f"How do the interest rates compare between {country1} and {country2} in {year}?"
                answer1 = f"In {year}, the interest rate in {country1} was {interest_rate1}% and in {country2} was {interest_rate2}%."
                questions.append(question1)
                ids.append(generate_id("CMP", combined_country_code, today_date, index))
                answers.append(answer1)
                falses.append("False")
                index += 1

    # Generate question to compare interest rate changes within the same country across years
    for k in range(len(years) - 1):
        year1 = years[k]
        year2 = years[k + 1]

        # Get interest rate data for consecutive years
        interest_rate_year1 = df.loc[df['geo\\TIME_PERIOD'] == country1, str(year1)].values[0]
        interest_rate_year2 = df.loc[df['geo\\TIME_PERIOD'] == country1, str(year2)].values[0]

        # Only proceed if both interest rates are available
        if pd.notna(interest_rate_year1) and pd.notna(interest_rate_year2):
            rate_change = round(interest_rate_year2 - interest_rate_year1, 2)
            question2 = f"How did the interest rate change in {country1} from {year1} to {year2}?"
            answer2 = f"The interest rate in {country1} changed by {rate_change}% between {year1} and {year2}."
            questions.append(question2)
            ids.append(generate_id("CMP", country_code1, today_date, index))
            answers.append(answer2)
            falses.append("False")
            index += 1

# Create the new DataFrame
questions_df = pd.DataFrame({
    "Question": questions,
    "ID": ids,
    "Answer": answers,
    "False": falses
})

# Save to CSV
questions_df.to_csv('IRT_LT_MCBY_A_comparison_questions.csv', index=False)
print("Comparison questions saved to IRT_LT_MCBY_A_comparison_questions.csv")

"""
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
"""



# List Questions: **LST**
def list_years_of_high_interest_rates(country: str, threshold: float) -> tuple:
    """
    Lists years where interest rates were above a given threshold.
    """
    question = f"Which years did {country} have an interest rate above {threshold}%?"
    # List years logic
    answer = f"{country} had interest rates above {threshold}% in the years: [years]."
    return question, answer

def list_countries_with_positive_interest_in_year(year: int) -> tuple:
    """
    Lists countries with positive interest rates in a specific year.
    """
    question = f"Which countries had positive interest rates in {year}?"
    answer = f"The countries with positive interest rates in {year} were: [countries]."
    return question, answer

import pandas as pd
from datetime import datetime

# Load the cleaned data
df = pd.read_csv('IRT_LT_MCBY_A_curated.csv')  

# Define today's date for the question IDs
today_date = datetime.now().strftime("%d/%m/%Y")

# List of countries and years in the dataset
countries = df['geo\\TIME_PERIOD'].dropna().unique()  # Ensure no NaN values in the countries list
years = [int(y) for y in df.columns[1:]]  # Convert years to integers for easier filtering

# Helper function to format the question ID
def generate_id(question_type, code, date, index):
    return f"IRT_LT_MCBY_A-{question_type}-{code}-{date}-{index:02d}"

# Lists to store generated question data
questions = []
ids = []
answers = []
falses = []

# Threshold value for the high-interest rate question
threshold = 5.0
index = 1

# Generate List questions for years with high interest rates by country
for country in countries:
    # Generate the 2-letter code from the country name
    country_code = ''.join([word[0] for word in country.split()]).upper()
    
    # Find years where interest rate was above the threshold
    high_interest_years = []
    for year in years:
        interest_rate = df.loc[df['geo\\TIME_PERIOD'] == country, str(year)].values[0]
        if pd.notna(interest_rate) and interest_rate > threshold:
            high_interest_years.append(year)
    
    # If there are years with high interest rates, generate the question
    if high_interest_years:
        question1 = f"Which years did {country} have an interest rate above {threshold}%?"
        answer1 = f"{country} had interest rates above {threshold}% in the years: {', '.join(map(str, high_interest_years))}."
        questions.append(question1)
        ids.append(generate_id("LST", country_code, today_date, index))
        answers.append(answer1)
        falses.append("False")
        index += 1

# Generate List questions for countries with positive interest rates in each year
for year in years:
    positive_interest_countries = []
    
    # Find countries with positive interest rates for the given year
    for country in countries:
        interest_rate = df.loc[df['geo\\TIME_PERIOD'] == country, str(year)].values[0]
        if pd.notna(interest_rate) and interest_rate > 0:
            positive_interest_countries.append(country)
    
    # If there are countries with positive interest rates, generate the question
    if positive_interest_countries:
        question2 = f"Which countries had positive interest rates in {year}?"
        answer2 = f"The countries with positive interest rates in {year} were: {', '.join(positive_interest_countries)}."
        questions.append(question2)
        ids.append(generate_id("LST", str(year), today_date, index))
        answers.append(answer2)
        falses.append("False")
        index += 1

# Create the new DataFrame
questions_df = pd.DataFrame({
    "Question": questions,
    "ID": ids,
    "Answer": answers,
    "False": falses
})

# Save to CSV
questions_df.to_csv('IRT_LT_MCBY_A_list_questions.csv', index=False)
print("List questions saved to IRT_LT_MCBY_A_list_questions.csv")


"""
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
"""

# Where Questions: **WHR**
def where_highest_interest_rate_in_year(year: int) -> tuple:
    """
    Finds the country with the highest interest rate in a specific year.
    """
    question = f"Where was the highest interest rate in {year}?"
    answer = f"The highest interest rate in {year} was in COUNTRY."
    return question, answer

def where_negative_interest_rate_occurred(year: int) -> tuple:
    """
    Finds countries with negative interest rates in a specific year.
    """
    question = f"Where were interest rates negative in {year}?"
    answer = f"In {year}, interest rates were negative in the following countries: [countries]."
    return question, answer

import pandas as pd
from datetime import datetime

# Load the cleaned data
df = pd.read_csv('IRT_LT_MCBY_A_curated.csv')  

# Define today's date for the question IDs
today_date = datetime.now().strftime("%d/%m/%Y")

# List of years in the dataset
years = [int(y) for y in df.columns[1:]]  # Convert years to integers for easier filtering

# Helper function to format the question ID
def generate_id(question_type, year, date, index):
    return f"IRT_LT_MCBY_A-{question_type}-YR{year}-{date}-{index:02d}"

# Lists to store generated question data
questions = []
ids = []
answers = []
falses = []

index = 1

# Generate Where questions for the highest interest rate in each year
for year in years:
    # Get interest rates for all countries in the specified year
    year_data = df[['geo\\TIME_PERIOD', str(year)]].dropna()
    if not year_data.empty:
        # Find the country with the highest interest rate
        max_rate_row = year_data.loc[year_data[str(year)].idxmax()]
        country_max = max_rate_row['geo\\TIME_PERIOD']
        max_rate = max_rate_row[str(year)]

        question1 = f"Where was the highest interest rate in {year}?"
        answer1 = f"The highest interest rate in {year} was in {country_max} with a rate of {max_rate}%."
        questions.append(question1)
        ids.append(generate_id("WHR", year, today_date, index))
        answers.append(answer1)
        falses.append("False")
        index += 1

# Generate Where questions for countries with negative interest rates in each year
for year in years:
    # Find countries with negative interest rates for the given year
    year_data = df[['geo\\TIME_PERIOD', str(year)]].dropna()
    negative_countries = year_data[year_data[str(year)] < 0]['geo\\TIME_PERIOD'].tolist()
    
    if negative_countries:
        question2 = f"Where were interest rates negative in {year}?"
        answer2 = f"In {year}, interest rates were negative in the following countries: {', '.join(negative_countries)}."
        questions.append(question2)
        ids.append(generate_id("WHR", year, today_date, index))
        answers.append(answer2)
        falses.append("False")
        index += 1

# Create the new DataFrame
questions_df = pd.DataFrame({
    "Question": questions,
    "ID": ids,
    "Answer": answers,
    "False": falses
})

# Save to CSV
questions_df.to_csv('IRT_LT_MCBY_A_where_questions.csv', index=False)
print("Where questions saved to IRT_LT_MCBY_A_where_questions.csv")


"""
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
"""


# When Questions: **WHE**
def year_with_lowest_interest_rate(country: str) -> tuple:
    """
    Finds the year with the lowest interest rate for a specific country.
    """
    question = f"When did {country} experience its lowest interest rate?"
    answer = f"The lowest interest rate in {country} occurred in YEAR."
    return question, answer

def year_highest_interest_rate_in_country(country: str) -> tuple:
    """
    Finds the year with the highest interest rate for a specific country.
    """
    question = f"When did {country} have its highest interest rate?"
    answer = f"The highest interest rate in {country} was in YEAR."
    return question, answer

import pandas as pd
from datetime import datetime

# Load the cleaned data
df = pd.read_csv('IRT_LT_MCBY_A_curated.csv')  

# Define today's date for the question IDs
today_date = datetime.now().strftime("%d/%m/%Y")

# List of countries and years in the dataset
countries = df['geo\\TIME_PERIOD'].dropna().unique()  # Ensure no NaN values in the countries list
years = [int(y) for y in df.columns[1:]]  # Convert years to integers for easier filtering

# Helper function to format the question ID
def generate_id(question_type, country_code, date, index):
    return f"IRT_LT_MCBY_A-{question_type}-{country_code}-{date}-{index:02d}"

# Lists to store generated question data
questions = []
ids = []
answers = []
falses = []

index = 1

# Generate When questions for the lowest and highest interest rates for each country
for country in countries:
    # Generate the 2-letter code from the country name
    country_code = ''.join([word[0] for word in country.split()]).upper()
    
    # Extract interest rate data for the country across all years
    country_data = df.loc[df['geo\\TIME_PERIOD'] == country, df.columns[1:]].dropna(axis=1)

    if not country_data.empty:
        # Find the year with the lowest interest rate
        min_year = country_data.idxmin(axis=1).values[0]
        min_rate = country_data.min(axis=1).values[0]

        question1 = f"When did {country} experience its lowest interest rate?"
        answer1 = f"The lowest interest rate in {country} occurred in {min_year} with a rate of {min_rate}%."
        questions.append(question1)
        ids.append(generate_id("WHE", country_code, today_date, index))
        answers.append(answer1)
        falses.append("False")
        index += 1

        # Find the year with the highest interest rate
        max_year = country_data.idxmax(axis=1).values[0]
        max_rate = country_data.max(axis=1).values[0]

        question2 = f"When did {country} have its highest interest rate?"
        answer2 = f"The highest interest rate in {country} was in {max_year} with a rate of {max_rate}%."
        questions.append(question2)
        ids.append(generate_id("WHE", country_code, today_date, index))
        answers.append(answer2)
        falses.append("False")
        index += 1

# Create the new DataFrame
questions_df = pd.DataFrame({
    "Question": questions,
    "ID": ids,
    "Answer": answers,
    "False": falses
})

# Save to CSV
questions_df.to_csv('IRT_LT_MCBY_A_when_questions.csv', index=False)
print("When questions saved to IRT_LT_MCBY_A_when_questions.csv")

"""
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
================================================================================================================================================================================================================================
"""





import pandas as pd
from datetime import datetime

# Define today's date for the question IDs
today_date = datetime.now().strftime("%d/%m/%Y")

# Helper function to format the question ID
def generate_id(question_type, code, date, index):
    return f"IRT_LT_MCBY_A-{question_type}-{code}-{date}-{index:02d}"

# Main function to generate all questions and save to CSV
def generate_definitions_mcby_questions():
    # Lists to store generated question data
    questions = []
    ids = []
    answers = []
    falses = []

    index = 1

    # Dictionary of questions and answers
    qa_pairs = {
        # Definition questions
        "What is an interest rate?": "An interest rate is the percentage charged on a loan or earned on savings over a period of time.",
        "What is the difference between real and nominal interest rates?": "Nominal interest rates are stated without adjustment for inflation, while real interest rates are adjusted to remove the effects of inflation.",
        "What is a nominal interest rate?": "A nominal interest rate is the rate of interest before adjusting for inflation.",
        "What is a real interest rate?": "A real interest rate is the interest rate adjusted to remove the effects of inflation.",
        "What is an annual interest rate?": "An annual interest rate is the percentage of interest charged or earned over one year.",
        "What is the Federal Funds Rate?": "The Federal Funds Rate is the interest rate at which banks lend to each other overnight, set by the U.S. Federal Reserve.",
        "What is a benchmark interest rate?": "A benchmark interest rate is a standard rate that guides other interest rates in an economy.",
        "What is a fixed interest rate?": "A fixed interest rate remains constant over the life of a loan or investment.",
        "What is a variable interest rate?": "A variable interest rate fluctuates over time based on market conditions.",
        "What is the discount rate?": "The discount rate is the interest rate used by central banks to lend to commercial banks.",
        "What is compound interest?": "Compound interest is the interest calculated on both the initial principal and the accumulated interest from previous periods.",
        "What is simple interest?": "Simple interest is the interest calculated only on the principal amount, without compounding.",
        "What is interest rate risk?": "Interest rate risk is the potential loss due to changes in interest rates affecting investments and loans.",
        "What is an interest rate spread?": "An interest rate spread is the difference between interest rates on loans and deposits, often indicating bank profitability.",
        "What is an interest rate ceiling?": "An interest rate ceiling is the maximum allowable interest rate, often set by regulation.",
        "What is an interest rate floor?": "An interest rate floor is the minimum allowable interest rate, typically used in adjustable-rate loans.",
        "What is a yield curve?": "A yield curve is a graph showing interest rates of bonds with differing maturities, indicating economic expectations.",
        "What is an inverted yield curve?": "An inverted yield curve occurs when short-term interest rates are higher than long-term rates, often predicting economic downturns.",
        "What is interest rate parity?": "Interest rate parity is a theory where exchange rates adjust to equalize the interest rates between two countries.",
        "What is a prime rate?": "The prime rate is the interest rate that banks offer to their most creditworthy customers.",
        "What is LIBOR?": "LIBOR, or the London Interbank Offered Rate, was a benchmark rate at which major global banks lent to each other, now replaced by other rates.",
        "What is SOFR?": "SOFR, or the Secured Overnight Financing Rate, is a benchmark rate that replaced LIBOR, based on overnight transactions in the U.S. Treasury market.",
        
        # MCBY-specific questions
        "What does 'MCBY' stand for?": "MCBY likely stands for 'Market Capitalization Bond Yield' or another classification related to government bond yields. Checking the dataset documentation can provide more details.",
        "What type of interest rates are represented by 'MCBY' in this dataset?": "'MCBY' likely refers to long-term government bond yields or benchmark interest rates, which reflect the market's expectation of economic conditions.",
        "How is 'MCBY' data commonly used in economic analysis?": "'MCBY' data, representing long-term bond yields, is often used to assess economic stability, inflation expectations, and fiscal policy impact.",
        "Which countries have the highest 'MCBY' rates over the years?": "Analyzing the dataset to find the countries with the highest 'MCBY' rates can indicate where bond yields were most elevated, suggesting economic stress or high inflation expectations.",
        "How did 'MCBY' rates change over time for Eurozone countries?": "'MCBY' rates for Eurozone countries can reveal the impact of ECB policies and economic convergence across member states.",
        "What is the average 'MCBY' rate for EU countries from 2000 to 2020?": "Calculating the average 'MCBY' rate for EU countries over this period provides insight into overall economic conditions within the EU.",
        "Are there significant differences in 'MCBY' rates between Eurozone and non-Eurozone countries?": "Comparing 'MCBY' rates between Eurozone and non-Eurozone countries can show the effects of shared monetary policy versus independent policies.",
        "How does 'MCBY' data correlate with inflation rates in these countries?": "'MCBY' rates often have a correlation with inflation, as bond yields reflect market inflation expectations.",
        "What factors influence changes in 'MCBY' rates?": "'MCBY' rates are influenced by inflation, central bank policy, fiscal stability, and market demand for long-term government bonds.",
        "Can 'MCBY' data be used to predict future economic downturns?": "Yes, 'MCBY' data, especially if it rises sharply, can sometimes indicate market fears of an economic downturn due to higher long-term borrowing costs.",

        # Interest Rate Basics
        "What is an interest rate?": "An interest rate is the percentage charged on a loan or earned on savings over a period of time.",
        "What is a fixed interest rate?": "A fixed interest rate remains constant over the life of a loan or investment.",
        "What is a variable interest rate?": "A variable interest rate fluctuates over time based on market conditions.",
        "What is compound interest?": "Compound interest is the interest calculated on both the initial principal and the accumulated interest from previous periods.",
        "What is simple interest?": "Simple interest is the interest calculated only on the principal amount, without compounding.",
    
        # Inflation and Interest Rates
        "What is the relationship between inflation and interest rates?": "Generally, when inflation rises, interest rates are increased to control inflation, as higher rates discourage borrowing and spending.",
        "What is a real interest rate?": "A real interest rate is the nominal interest rate adjusted to remove the effects of inflation.",
        "How does inflation affect savings?": "Inflation erodes the purchasing power of money, meaning savings lose value over time if interest rates are below the inflation rate.",
        "What are nominal interest rates?": "Nominal interest rates are stated without adjustment for inflation, reflecting the 'face' rate seen on financial products.",
    
        # Central Banks and Policy
        "What is the role of a central bank?": "Central banks manage monetary policy, control inflation, regulate banks, and act as a lender of last resort in a financial crisis.",
        "What is the Federal Reserve?": "The Federal Reserve, or Fed, is the central bank of the United States, managing interest rates, inflation, and overall financial stability.",
        "What is the ECB?": "The European Central Bank (ECB) manages monetary policy for the Eurozone, aiming to maintain price stability and economic growth.",
        "How do central banks influence interest rates?": "Central banks influence interest rates by setting benchmark rates, controlling money supply, and using open market operations.",
        "What is quantitative easing?": "Quantitative easing (QE) is a monetary policy where central banks purchase securities to inject liquidity into the economy, often lowering interest rates.",
        "What is tapering in monetary policy?": "Tapering refers to the gradual reduction of central bank asset purchases, often leading to an increase in interest rates.",
    
        # Economic Indicators
        "What is GDP?": "Gross Domestic Product (GDP) measures the total economic output of a country over a period of time.",
        "How does GDP growth affect interest rates?": "Strong GDP growth may lead central banks to raise interest rates to control inflation, while slow growth often leads to lower rates.",
        "What is the Consumer Price Index (CPI)?": "CPI is a measure of inflation that tracks the change in prices for a basket of consumer goods and services over time.",
        "What is the unemployment rate?": "The unemployment rate is the percentage of the labor force that is unemployed and actively seeking employment.",
        "How does unemployment affect interest rates?": "High unemployment can lead central banks to lower rates to encourage economic activity, while low unemployment may result in rate hikes to control inflation.",
    
        # Bonds and Yields
        "What is a bond?": "A bond is a fixed-income security where an investor loans money to an issuer, typically a corporation or government, for a defined period at a specified interest rate.",
        "What is a bond yield?": "Bond yield is the return an investor earns on a bond, expressed as a percentage of its current price or face value.",
        "What is a government bond?": "A government bond is a debt security issued by a government to fund government spending, considered low-risk due to the government backing.",
        "What is the relationship between bond prices and interest rates?": "Bond prices and interest rates are inversely related; when rates rise, bond prices fall, and vice versa.",
        "What is the yield curve?": "A yield curve is a graph showing the relationship between bond yields and maturities, indicating market expectations for interest rates.",
    
        # Exchange Rates and International Finance
        "What is an exchange rate?": "An exchange rate is the price of one currency in terms of another, impacting trade and investment flows.",
        "How do interest rates affect exchange rates?": "Higher interest rates attract foreign capital, increasing demand for a currency and strengthening its value, while lower rates may weaken it.",
        "What is a floating exchange rate?": "A floating exchange rate is determined by market forces, where currency value fluctuates based on supply and demand.",
        "What is a fixed exchange rate?": "A fixed exchange rate is set by a government or central bank and is maintained against another currency or a basket of currencies.",
        "What is interest rate parity?": "Interest rate parity is a theory suggesting that exchange rate changes reflect differences in interest rates between two countries.",
    
        # Market Concepts
        "What is a stock?": "A stock is a type of security representing ownership in a corporation, entitling the shareholder to a portion of the company's assets and earnings.",
        "What is a stock market index?": "A stock market index tracks the performance of a group of stocks, reflecting the general direction of the market or specific sectors.",
        "What is market capitalization?": "Market capitalization is the total value of a company's outstanding shares, calculated as share price multiplied by total shares.",
        "What is a bull market?": "A bull market is a period of rising stock prices, often accompanied by high investor confidence and expectations of continued growth.",
        "What is a bear market?": "A bear market is a period of declining stock prices, often accompanied by pessimism and expectations of a prolonged downturn.",
    
        # Risk Management
        "What is credit risk?": "Credit risk is the possibility that a borrower will fail to repay a loan, impacting lenders and investors who face potential losses.",
        "What is market risk?": "Market risk is the potential financial loss from changes in market prices, including stocks, bonds, and commodities.",
        "What is liquidity risk?": "Liquidity risk is the risk that an asset cannot be sold quickly enough to prevent a loss, often due to a lack of market buyers.",
        "What is interest rate risk?": "Interest rate risk is the potential for investment losses due to fluctuations in interest rates.",
        "What is inflation risk?": "Inflation risk is the potential loss of purchasing power as inflation erodes the value of cash and fixed-income investments over time.",
    
        # Other Financial Terms
        "What is a mortgage?": "A mortgage is a loan used to purchase property, where the property itself acts as collateral for the loan.",
        "What is refinancing?": "Refinancing is the process of replacing an existing loan with a new one, often to take advantage of lower interest rates.",
        "What is leverage?": "Leverage is the use of borrowed capital for an investment, aiming to increase the potential return on investment.",
        "What is a hedge fund?": "A hedge fund is an investment fund that uses a variety of strategies to generate returns, often for high-net-worth individuals and institutional investors.",
        "What is private equity?": "Private equity involves investing in private companies or buying out public companies to restructure and improve their value before resale.",
        "What is venture capital?": "Venture capital is financing provided to startups and small businesses with high growth potential in exchange for equity.",
        "What is an IPO?": "An Initial Public Offering (IPO) is when a company offers shares to the public for the first time, typically to raise capital for expansion.",
        "What is ESG investing?": "Environmental, Social, and Governance (ESG) investing considers non-financial factors to assess the sustainability and social impact of an investment.",
        "What is financial leverage?": "Financial leverage is the use of borrowed funds to increase the return on investment, which can amplify gains or losses.",
        "What is asset allocation?": "Asset allocation is an investment strategy that spreads investments across different asset classes to balance risk and return.",
        "What is diversification?": "Diversification is a risk management strategy that involves spreading investments across various assets to reduce exposure to any one asset."
    }
    
    # Generate questions and answers from qa_pairs
    for question, answer in qa_pairs.items():
        questions.append(question)
        ids.append(generate_id("DEF", "GEN", today_date, index))
        answers.append(answer)
        falses.append("False")
        index += 1

    # Create DataFrame
    questions_df = pd.DataFrame({
        "Question": questions,
        "ID": ids,
        "Answer": answers,
        "False": falses
    })

    # Save to CSV
    questions_df.to_csv('IRT_LT_MCBY_A_definitions_mcby_questions.csv', index=False)
    print("Definitions and MCBY-related questions saved to IRT_LT_MCBY_A_definitions_mcby_questions.csv")

# Run the function to generate the CSV file
generate_definitions_mcby_questions()