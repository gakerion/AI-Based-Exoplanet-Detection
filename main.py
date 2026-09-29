import pandas as pd
import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig
)

# ============================================================
# 1. SETTINGS
# ============================================================

MODEL_NAME = "AstroMLab/AstroSage-8B"
CSV_FILE = "cumulative_copy.csv"

LABELS = [
    "confirmed exoplanet",
    "exoplanet candidate",
    "false positive"
]


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
print("Device map:")
