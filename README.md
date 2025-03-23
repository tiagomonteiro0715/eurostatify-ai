## EuroStatify AI — Open Source

- EuroStatify AI was created to make European public data more accessible and useful for researchers, policymakers, and civic technologists.

- It leverages a fine-tuned Google T5 model trained on 150,000+ custom-generated question–answer pairs derived from Eurostat datasets.

- This project aimed to bridge the gap between complex institutional data and real-world decision-making tools. 

- It is now fully open source!

## Project Structure
```

EuroStatify-AI/
├── EuroStatify-AI-OpenSource-data-generating-files/
│   ├── filter_base_data.py
│   ├── filter_eurostat_dataset.py
│   ├── fetch_and_save_eurostat.py
│   ├── generate_questions_apro_mt_pann.py
│   ├── generate_questions_irt_lt_mcby_a.py
│   ├── generate_questions_nasa_10_ki.py
│   ├── generate_dataset_json.py
│   └── main_training_pipeline.py
│
├── eurostatify-AI-t5-model-finetuned/
│   ├── adapter_model.safetensors
│   ├── adapter_config.json
│   ├── tokenizer_config.json
│   ├── special_tokens_map.json
│   ├── added_tokens.json
│   └── spiece.model

```

## Features

- Fine-tuned Google T5 model on Eurostat datasets

- Over 150,000 custom Q&A pairs generated using Python scripts

- Custom data filtering, transformation, and question-generation tools

- Framer-built front-end (not included in this release)

- Fully open-source business strategy and technical planning

## How It Works


1. Prepare and Filter Data
```
Use the scripts in EuroStatify-AI-OpenSource-data-generating-files/ to fetch, filter, and clean Eurostat data.

python fetch_and_save_eurostat.py
python filter_eurostat_dataset.py
```
2. Generate QA Pairs from Eurostat Datasets
```
Each generate_questions_*.py file corresponds to a specific Eurostat dataset. These generate structured question–answer pairs.

python generate_questions_apro_mt_pann.py

You can modify or duplicate these scripts to apply the logic to new datasets.
```
3. Build the Dataset for Fine-Tuning
```
Merge and structure your questions into the correct JSON format:

python generate_dataset_json.py
```
4. Train or Reuse the Fine-Tuned Model
```
Use the included main_training_pipeline.py to load the training dataset and fine-tune the T5 model.

The fine-tuned model is available in:

eurostatify-AI-t5-model-finetuned/

This includes:

    adapter_model.safetensors — weights

    Tokenizer configs

    Custom token handling
```
## Load Fine-Tuned T5 in Python

```
from transformers import T5Tokenizer, T5ForConditionalGeneration

model_path = "./eurostatify-AI-t5-model-finetuned"
tokenizer = T5Tokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path)

input_text = "What is the milk production in Germany in 2020?"
inputs = tokenizer(input_text, return_tensors="pt")
outputs = model.generate(**inputs)
answer = tokenizer.decode(outputs[0])
print(answer)

```

## Requirements

- Python 3.8+

- Transformers (pip install transformers)

- Pandas, requests, tqdm, etc. (see requirements.txt)

## Example Use Case

    “Show me the employment rate of women in Finland between 2010 and 2020.”
    → The model will fetch and interpret data trends based on the Eurostat source and generate a readable answer.

## Business & Strategy

We’ve also open-sourced the original business plan, product notes, and strategic frameworks that guided the development of EuroStatify AI.

- Business Plan PDF
- Includes Blue Ocean Strategy, SaaS metrics, marketing, and financial modeling.

### Feel free to fork, adapt, or build on this project — especially if you're working in:

- Public data transparency

- NLP for governance

- AI-powered dashboards

## License

This project is released under the MIT License.
Use it freely, modify it openly, and credit when appropriate.


## Credits

    Built by Tiago Monteiro

    Powered by open data from Eurostat

    Front-end built with Framer
