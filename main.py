from transformers import pipeline , BitsAndBytesConfig
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

classifier = pipeline(
    "zero-shot-classification",
    model="AstroMLab/AstroSage-8B",
    device=0,
    model_kwargs={
        "quantization_config": quant_config
    }
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

    result = classifier(
        star_text,
        candidate_labels=candidate_labels
    )

    # -----------------------------
    # 8. Display result
    # -----------------------------

    print("\nAI prediction:")
    print(result["labels"][0])

    print("AI score:")
    print(result["scores"][0])
