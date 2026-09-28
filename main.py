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


# ============================================================
# 5. LOAD DATASET
# ============================================================

df = pd.read_csv(CSV_FILE)

print(f"\nLoaded {len(df)} candidates.")


# ============================================================
# 6. FUNCTION TO CALCULATE LABEL PROBABILITIES
# ============================================================

def classify_candidate(prompt):

    # --------------------------------------------------------
    # Tokenize the prompt
    # --------------------------------------------------------

    prompt_tokens = tokenizer(
        prompt,
        return_tensors="pt"
    )

    input_ids = prompt_tokens["input_ids"].to(model.device)
    attention_mask = prompt_tokens["attention_mask"].to(model.device)

    scores = {}

    # --------------------------------------------------------
    # Calculate probability of each possible answer
    # --------------------------------------------------------

    for label in LABELS:

        # Tokenize candidate label
        label_tokens = tokenizer(
            label,
            add_special_tokens=False,
            return_tensors="pt"
        )["input_ids"].to(model.device)

        # Combine:
        #
        # prompt + candidate label
        #
        combined_ids = torch.cat(
            [input_ids, label_tokens],
            dim=1
        )

        combined_attention = torch.ones_like(
            combined_ids
        )

        with torch.inference_mode():

            outputs = model(
                input_ids=combined_ids,
                attention_mask=combined_attention
            )

            logits = outputs.logits

        # ----------------------------------------------------
        # We only care about the logits corresponding
        # to the label tokens.
        # ----------------------------------------------------

        prompt_length = input_ids.shape[1]

        label_length = label_tokens.shape[1]

        label_logits = logits[
            0,
            prompt_length - 1:
            prompt_length + label_length - 1,
            :
        ]

        # ----------------------------------------------------
        # Convert logits to log probabilities
        # ----------------------------------------------------

        log_probs = torch.log_softmax(
            label_logits,
            dim=-1
        )

        # ----------------------------------------------------
        # Get probability of the actual label tokens
        # ----------------------------------------------------

        token_log_probs = []

        for i in range(label_length):

            token_id = label_tokens[0, i]

            token_log_prob = log_probs[
                i,
                token_id
            ]

            token_log_probs.append(
                token_log_prob
            )

        # ----------------------------------------------------
        # Average log probability across the label tokens.
        #
        # Averaging prevents longer labels from being
        # automatically penalized.
        # ----------------------------------------------------

        mean_log_probability = torch.stack(
            token_log_probs
        ).mean()

        scores[label] = mean_log_probability.item()

    # ========================================================
    # Convert the three scores into percentages
    # ========================================================

    score_tensor = torch.tensor(
        list(scores.values())
    )

    probabilities = torch.softmax(
        score_tensor,
        dim=0
    )

    probabilities = probabilities.tolist()

    results = {
        label: probability * 100
        for label, probability
        in zip(LABELS, probabilities)
    }

    return results


# ============================================================
# 7. PROCESS EVERY CANDIDATE
# ============================================================

results = []

for index, row in df.iterrows():

    print("\n" + "=" * 70)
    print(f"CANDIDATE {index + 1} / {len(df)}")
    print(f"KEPID: {row['kepid']}")
    print(f"KOI:   {row['kepoi_name']}")
    print("=" * 70)

    # --------------------------------------------------------
    # Create astronomical description
    #
    # IMPORTANT:
    # koi_disposition is NOT included here.
    # --------------------------------------------------------

    prompt = f"""
You are analyzing a Kepler astronomical transit candidate.

Use the following observed properties to assess the candidate.

Orbital period: {row['koi_period']:.4f} days
Transit duration: {row['koi_duration']:.4f} hours
Transit depth: {row['koi_depth']:.4f} ppm
Planet radius: {row['koi_prad']:.4f} Earth radii
Stellar radius: {row['koi_srad']:.4f} Solar radii
Impact parameter: {row['koi_impact']:.4f}
Transit signal-to-noise ratio: {row['koi_model_snr']:.4f}
Equilibrium temperature: {row['koi_teq']:.4f} K
Stellar effective temperature: {row['koi_steff']:.2f} K
Stellar surface gravity: {row['koi_slogg']:.4f}

Which classification best describes this candidate?

Answer:
"""

    # --------------------------------------------------------
    # Get probabilities
    # --------------------------------------------------------

    probabilities = classify_candidate(prompt)

    # --------------------------------------------------------
    # Find highest probability
    # --------------------------------------------------------

    prediction = max(
        probabilities,
        key=probabilities.get
    )

    # --------------------------------------------------------
    # Actual ground truth
    # --------------------------------------------------------

    actual = str(
        row["koi_disposition"]
    ).strip().upper()

    # Convert dataset label to our label format
    if actual == "CONFIRMED":
        actual_label = "confirmed exoplanet"

    elif actual == "CANDIDATE":
        actual_label = "exoplanet candidate"

    elif actual == "FALSE POSITIVE":
        actual_label = "false positive"

    else:
        actual_label = actual

    # --------------------------------------------------------
    # Print probabilities
    # --------------------------------------------------------

    print("\nAI probabilities:")

    for label, probability in probabilities.items():

        print(
            f"{label:<25} "
            f"{probability:6.2f}%"
        )

    print("\nAI prediction:")
    print(prediction)

    print("\nActual dataset classification:")
    print(actual_label)

    # --------------------------------------------------------
    # Check prediction
    # --------------------------------------------------------

    correct = (
        prediction.lower()
        == actual_label.lower()
    )

    print("\nResult:")

    if correct:
        print("CORRECT")
    else:
        print("INCORRECT")

    # --------------------------------------------------------
    # Save result
    # --------------------------------------------------------

    results.append({
        "rowid": row["rowid"],
        "kepid": row["kepid"],
        "kepoi_name": row["kepoi_name"],

        "AI_prediction": prediction,

        "confirmed_probability":
            probabilities["confirmed exoplanet"],

        "candidate_probability":
            probabilities["exoplanet candidate"],

        "false_positive_probability":
            probabilities["false positive"],

        "actual_classification":
            actual_label,

        "correct":
            correct
    })


# ============================================================
# 8. SAVE RESULTS
# ============================================================

results_df = pd.DataFrame(results)

results_df.to_csv(
    "astrosage_predictions.csv",
    index=False
)

print("\n" + "=" * 70)
print("FINISHED")
print("=" * 70)

# ============================================================
# 9. OVERALL ACCURACY
# ============================================================

accuracy = (
    results_df["correct"].mean()
    * 100
)

print(
    f"\nAccuracy: {accuracy:.2f}%"
)

print(
    "\nResults saved to: "
    "astrosage_predictions.csv"
)