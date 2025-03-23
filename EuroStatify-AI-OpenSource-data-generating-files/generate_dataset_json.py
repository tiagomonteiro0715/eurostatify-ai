import os
import json
import pandas as pd

def create_squad_json(output_file="database.json"):
    squad_data = {
        "version": "v1.0",
        "data": []
    }

    # Loop over each file in the current directory
    for filename in os.listdir():
        # Only process files that start with the specific prefixes and have .csv extension
        if (filename.startswith("IRT_LT_MCBY_A_c") or filename.startswith("NASA_10_KI_")) and filename.endswith(".csv"):
            # Use the filename (without extension) as the title
            title = filename.split('.')[0]

            # Read the CSV file into a DataFrame
            df = pd.read_csv(filename)

            # Prepare the Q&A structure without 'context'
            paragraphs = []
            qas_list = []
            for _, row in df.iterrows():
                question = row['Question']
                answer_text = row['Answer']
                is_false = row['False']  # assuming the column name is "False"
                
                # Each question will have one Q&A pair in SQuAD format without context
                qas_list.append({
                    "question": question,
                    "id": row['ID'],
                    "is_impossible": bool(is_false),  # Assuming "False" means if the answer is false or not
                    "answers": [{
                        "text": answer_text,
                        "answer_start": 0  # Just to keep structure, answer_start is arbitrary
                    }]
                })

            # Append each file's data as a new title entry in the JSON structure
            squad_data["data"].append({
                "title": title,
                "qas": qas_list  # Directly adding qas list without paragraphs or context
            })

    # Write the SQuAD-like JSON data to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(squad_data, f, ensure_ascii=False, indent=4)

# Run the function in the current directory
create_squad_json()
