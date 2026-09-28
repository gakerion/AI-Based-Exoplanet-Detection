# from transformers import pipeline , BitsAndBytesConfig
# import pandas as pd
# import torch

# quant_config = BitsAndBytesConfig(
#     load_in_4bit=True,
#     bnb_4bit_compute_dtype=torch.float16,
#     bnb_4bit_quant_type="nf4",
#     bnb_4bit_use_double_quant=True
# )

# # -----------------------------
# # 1. Load dataset
# # -----------------------------

# df = pd.read_csv("cumulative_copy.csv")


# # -----------------------------
# # 2. Load Hugging Face model
# # -----------------------------

# classifier = pipeline(
#     "zero-shot-classification",
#     model="AstroMLab/AstroSage-8B",
#     device=0,
#     model_kwargs={
#         "quantization_config": quant_config
#     }
# )

# # -----------------------------
# # 3. Possible classifications
# # -----------------------------

# candidate_labels = [
#     "confirmed exoplanet",
#     "exoplanet candidate",
#     "false positive"
# ]


# # -----------------------------
# # 4. Process each star
# # -----------------------------

# for kepid, star_data in df.groupby("kepid"):

#     print("\n" + "=" * 50)
#     print(f"STAR: {kepid}")
#     print(f"Number of candidates: {len(star_data)}")
#     print("=" * 50)

#     descriptions = []

#     # -------------------------
#     # 5. Process each candidate
#     # -------------------------

#     for _, row in star_data.iterrows():

#         description = (
#             f"This astronomical candidate has "
#             f"an orbital period of {row['koi_period']:.2f} days, "
#             f"a transit duration of {row['koi_duration']:.2f} hours, "
#             f"a transit depth of {row['koi_depth']:.2f} ppm, "
#             f"an estimated planet radius of {row['koi_prad']:.2f} Earth radii, "
#             f"and a stellar radius of {row['koi_srad']:.2f} solar radii."
#         )

#         descriptions.append(description)

#     # -----------------------------
#     # 6. Combine candidates
#     # -----------------------------

#     star_text = " ".join(descriptions)

#     print("\nInformation sent to AI:")
#     print(star_text)

#     # -----------------------------
#     # 7. Ask AI to classify it
#     # -----------------------------

#     result = classifier(
#         star_text,
#         candidate_labels=candidate_labels
#     )

#     # -----------------------------
#     # 8. Display result
#     # -----------------------------

#     print("\nAI prediction:")
#     print(result["labels"][0])

#     print("AI score:")
#     print(result["scores"][0])
import torch
import pandas as pd

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig
)

# ============================================================
# 1. 4-bit quantization configuration
# ============================================================

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

# ============================================================
# 2. Load tokenizer
# ============================================================

model_name = "AstroMLab/AstroSage-8B"

tokenizer = AutoTokenizer.from_pretrained(model_name)

# ============================================================
# 3. Load AstroSage in 4-bit
# ============================================================

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=quant_config,
    device_map="auto",
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True
)

model.eval()

# ============================================================
# 4. Load dataset
# ============================================================

df = pd.read_csv("cumulative_copy.csv")

# ============================================================
# 5. Allowed classifications
# ============================================================

candidate_labels = [
    "confirmed exoplanet",
    "exoplanet candidate",
    "false positive"
]

# ============================================================
# 6. Classify each candidate
# ============================================================

for _, row in df.iterrows():

    description = (
        f"An astronomical candidate has the following properties:\n"
        f"Orbital period: {row['koi_period']:.2f} days\n"
        f"Transit duration: {row['koi_duration']:.2f} hours\n"
        f"Transit depth: {row['koi_depth']:.2f} ppm\n"
        f"Estimated planet radius: {row['koi_prad']:.2f} Earth radii\n"
        f"Stellar radius: {row['koi_srad']:.2f} solar radii\n\n"
    )

    prompt = (
        "Classify this astronomical candidate into exactly ONE of these "
        "categories:\n"
        "- confirmed exoplanet\n"
        "- exoplanet candidate\n"
        "- false positive\n\n"
        f"{description}"
        "Answer with only the category name."
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    ).to(model.device)

    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=10,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

    # Only decode newly generated tokens
    generated_tokens = outputs[0][inputs["input_ids"].shape[1]:]

    answer = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    ).strip()

    print("=" * 60)
    print(f"KEPID: {row['kepid']}")
    print(f"Prediction: {answer}")