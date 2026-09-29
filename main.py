import csv
import random

import pandas as pd
import xgboost as xgb
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

df = pd.read_csv("Exo_predict.csv")



# ============================================================
# 2. Features used by XGBoost
# ============================================================

features = [
    "koi_period",
    "koi_impact",
    "koi_duration",
    "koi_depth",
    "koi_prad",
    "koi_teq",
    "koi_insol",
    "koi_model_snr",
    "koi_steff",
    "koi_slogg",
    "koi_srad",
    "koi_kepmag",
]


def get_random_kpids(filename):
    confirmed = []
    false_positive = []

    with open(filename, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            data = (row["kepid"], row["koi_disposition"])

            if row["koi_disposition"] == "CONFIRMED":
                confirmed.append(data)

            elif row["koi_disposition"] == "FALSE POSITIVE":
                false_positive.append(data)

    # Make sure we have at least one of each
    selected = [
        random.choice(confirmed),
        random.choice(false_positive)
    ]

    # Combine the two categories
    remaining = confirmed + false_positive

    # Remove the two already selected
    remaining.remove(selected[0])
    remaining.remove(selected[1])

    # Pick 3 more
    selected += random.sample(remaining, 3)

    # Shuffle the result
    random.shuffle(selected)

    return selected