import os
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
from datasets import load_dataset, Dataset
import json
import pandas as pd

# Set the number of threads PyTorch should use for CPU parallelism
# This will utilize all available CPUs for training
os.environ["OMP_NUM_THREADS"] = "8"  # Adjust based on the number of physical cores in your system
os.environ["MKL_NUM_THREADS"] = "8"  # Adjust based on the number of physical cores in your system
os.environ["CPU_THREADS"] = "8"      # Adjust based on the number of physical cores in your system

# Load T5 Small model and tokenizer
model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Load your custom dataset (assuming it is in SQuAD-like JSON format)
with open("database.json", "r") as f:
    data = json.load(f)

def convert_to_hf_dataset(data):
    rows = []
    for item in data["data"]:
        for qa in item["qas"]:
            rows.append({
                "question": str(qa["question"]),
                "answer": str(qa["answers"][0]["text"])
            })
    # Convert to DataFrame with string types to avoid type issues
    df = pd.DataFrame(rows).astype(str)
    return Dataset.from_pandas(df)

# Load and convert the custom dataset
custom_dataset = convert_to_hf_dataset(data)

# Split into train and validation sets
train_test_split = custom_dataset.train_test_split(test_size=0.2)
train_dataset = train_test_split["train"]
val_dataset = train_test_split["test"]

# Preprocess custom data into T5 format
def preprocess_function(examples):
    input_texts = [
        f"question: {question}"
        for question in examples["question"]
    ]
    
    target_texts = examples["answer"]

    model_inputs = tokenizer(input_texts, max_length=512, truncation=True, padding="max_length")
    labels = tokenizer(target_texts, max_length=128, truncation=True, padding="max_length")

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

# Tokenize the dataset
tokenized_train = train_dataset.map(preprocess_function, batched=True)
tokenized_val = val_dataset.map(preprocess_function, batched=True)
print("Tokenized dataset created successfully.")

# Define PEFT configuration for LoRA
from peft import get_peft_model, LoraConfig

peft_config = LoraConfig(
    task_type="SEQ_2_SEQ_LM",   
    r=8,                        
    lora_alpha=16,              
    lora_dropout=0.1,           
)

# Apply PEFT to the model
model = get_peft_model(model, peft_config)

# Define training arguments
from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir="./t5_custom_finetuned",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    learning_rate=5e-5,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir='./logs',
    eval_strategy="epoch",
    save_strategy="epoch",
    # Ensure we are using CPU for training
    no_cuda=True,  # This forces the model to use the CPU
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_val
)

# Train the model
trainer.train()

# Directory for saving the model and tokenizer
output_dir = "./t5_custom_finetuned_saved"

# Create the directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Save the fine-tuned model and tokenizer
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)

print(f"Model and tokenizer saved to {output_dir}")

# Define a question for inference
question = "What is wrong?"

# Prepare the input text in T5's format
input_text = f"question: {question}"
inputs = tokenizer(input_text, return_tensors="pt")

# Generate the answer
with torch.no_grad():
    outputs = model.generate(inputs.input_ids, max_length=50, num_beams=5, early_stopping=True)

# Decode and print the answer
answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("Answer:", answer)
