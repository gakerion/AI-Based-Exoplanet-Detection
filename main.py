from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import pandas as pd
import torch

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True
)

# -----------------------------
# 1. Load dataset
# -----------------------------

df = pd.read_csv("cumulative_copy.csv")


# -----------------------------
# 2. Load Hugging Face model
# -----------------------------

model_name = "AstroMLab/AstroSage-8B"

tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    quantization_config=quant_config,
    torch_dtype=torch.float16
)


# -----------------------------
# 3. Possible classifications
# -----------------------------

candidate_labels = [
    "confirmed exoplanet",
    "exoplanet candidate",
    "false positive"
]


# -----------------------------
# 4. Process each star
# -----------------------------

for kepid, star_data in df.groupby("kepid"):

    print("\n" + "=" * 50)
    print(f"STAR: {kepid}")
    print(f"Number of candidates: {len(star_data)}")
    print("=" * 50)

    descriptions = []

    # -------------------------
    # 5. Process each candidate
    # -------------------------

    for _, row in star_data.iterrows():

        description = (
            f"This astronomical candidate has "
            f"an orbital period of {row['koi_period']:.2f} days, "
            f"a transit duration of {row['koi_duration']:.2f} hours, "
            f"a transit depth of {row['koi_depth']:.2f} ppm, "
            f"an estimated planet radius of {row['koi_prad']:.2f} Earth radii, "
            f"and a stellar radius of {row['koi_srad']:.2f} solar radii."
        )

        descriptions.append(description)

    # -----------------------------
    # 6. Combine candidates
    # -----------------------------

    star_text = " ".join(descriptions)

    print("\nInformation sent to AI:")
    print(star_text)

    # -----------------------------
    # 7. Ask AI to classify it
    # -----------------------------

    prompt = f"""
Classify the following astronomical candidate.

{star_text}

Choose exactly one classification:

{candidate_labels[0]}
{candidate_labels[1]}
{candidate_labels[2]}

Return only the classification.
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    ).to(model.device)

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=30,
            temperature=0.1,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

    generated_text = outputs[0][inputs["input_ids"].shape[-1]:]

    result = tokenizer.decode(
        generated_text,
        skip_special_tokens=True
    ).strip()

    # -----------------------------
    # 8. Display result
    # -----------------------------

    print("\nAI prediction:")
    print(result)