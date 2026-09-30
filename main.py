import helper


import pandas as pd

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig
)


MODEL_NAME = "AstroMLab/AstroSage-8B"



# ============================================================
# 2. 4-BIT QUANTIZATION
# ============================================================

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)


# ============================================================
# 3. LOAD TOKENIZER
# ============================================================

print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token


# ============================================================
# 4. LOAD MODEL
# ============================================================

print("Loading AstroSage-8B in 4-bit...")

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    quantization_config=quant_config,
    device_map="auto",
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True
)

model.eval()

print("Model loaded.")


# ============================================================
# 1. Load dataset
# ============================================================

def get_star_summary(kic_id):

    # Get all catalog data for this KIC ID
    star_data = helper.get_star_info(kic_id)

    prompt = f"""
You are an astronomy assistant.

Analyze the following catalog data for KIC {kic_id}:

{star_data}

Write ONE concise scientific summary in a single paragraph.

Rules:
- Use ONLY the data provided.
- Do not estimate or invent values.
- If a value is Unknown, state that it is unknown.
- Do not repeat the summary.
- Do not discuss future research or observations.
- Do not add a second paragraph.
- Do not include headings or formatting.
- STOP after the first paragraph.
"""

    # Tokenize prompt
    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    )

    inputs = {
        key: value.to(model.device)
        for key, value in inputs.items()
    }

    # Generate AstroSage response
    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=100,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

    # Remove prompt from generated output
    generated_tokens = outputs[0][
        inputs["input_ids"].shape[1]:
    ]

    summary = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    ).strip()

    return summary


# while(1):
#     kic = int(input("Enter KIC: "))
#     print(helper.get_star_info(kic))
#     print(get_star_summary(kic))