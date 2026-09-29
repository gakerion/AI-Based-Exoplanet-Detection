# ============================================================
# test_astrosage.py
#
# KIC ID
#   ↓
# NASA Exoplanet Archive
#   ↓
# radius / distance / metallicity
#
# KIC ID
#   ↓
# VizieR APOGEE/Kepler catalog
#   ↓
# oxygen abundance
#
# Retrieved values
#   ↓
# AstroSage-8B
#   ↓
# scientific response
# ============================================================

import requests
import pandas as pd
import io
import torch

from transformers import pipeline, BitsAndBytesConfig


# ============================================================
# 1. ASTROSAGE MODEL
# ============================================================

MODEL_NAME = "AstroMLab/AstroSage-8B"


# 4-bit quantization
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True
)


generator = pipeline(
    "text-generation",
    model=MODEL_NAME,
    model_kwargs={
        "quantization_config": quant_config
    },
    device_map="auto"
)


# ============================================================
# 2. NASA EXOPLANET ARCHIVE
# ============================================================

NASA_TAP_URL = (
    "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
)


def get_nasa_stellar_data(kic_id):

    query = f"""
        SELECT
            kepid,
            feh,
            radius,
            dist
        FROM keplerstellar
        WHERE kepid = {kic_id}
    """

    params = {
        "query": query,
        "format": "json"
    }

    try:

        response = requests.get(
            NASA_TAP_URL,
            params=params,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        if not data:
            return {
                "Metallicity": "Unknown",
                "Radius": "Unknown",
                "Distance": "Unknown"
            }

        row = data[0]

        return {
            "Metallicity": clean_value(row.get("feh")),
            "Radius": clean_value(row.get("radius")),
            "Distance": clean_value(row.get("dist"))
        }

    except Exception as e:

        print("NASA lookup error:", e)

        return {
            "Metallicity": "Unknown",
            "Radius": "Unknown",
            "Distance": "Unknown"
        }


# ============================================================
# 3. VIZIER OXYGEN CATALOG
# ============================================================

VIZIER_FIELD_URL = (
    "https://cdsarc.cds.unistra.fr/ftp/cats/J/A+A/594/A43/field.dat"
)


_vizier_field_data = None


def load_vizier_catalog():

    global _vizier_field_data

    if _vizier_field_data is not None:
        return _vizier_field_data

    try:

        response = requests.get(
            VIZIER_FIELD_URL,
            timeout=30
        )

        response.raise_for_status()

        # The VizieR file is fixed-width.
        #
        # According to the catalog documentation:
        #
        # KIC   : columns 20-27
        # [O/H] : columns 130-135
        #
        # Python uses zero-based indexing.

        lines = response.text.splitlines()

        records = []

        for line in lines:

            if len(line) < 135:
                continue

            try:

                kic = line[19:27].strip()
                oh = line[129:135].strip()

                if not kic:
                    continue

                kic = int(kic)

                if oh in ("", "-"):
                    oxygen = "Unknown"
                else:
                    oxygen = float(oh)

                records.append({
                    "KIC": kic,
                    "Oxygen": oxygen
                })

            except (ValueError, TypeError):
                continue

        _vizier_field_data = pd.DataFrame(records)

        return _vizier_field_data

    except Exception as e:

        print("VizieR lookup error:", e)

        return pd.DataFrame(
            columns=["KIC", "Oxygen"]
        )


def get_oxygen(kic_id):

    catalog = load_vizier_catalog()

    if catalog.empty:
        return "Unknown"

    match = catalog[
        catalog["KIC"] == int(kic_id)
    ]

    if match.empty:
        return "Unknown"

    oxygen = match.iloc[0]["Oxygen"]

    return clean_value(oxygen)


# ============================================================
# 4. CLEAN VALUES
# ============================================================

def clean_value(value):

    if value is None:
        return "Unknown"

    if isinstance(value, float):

        if pd.isna(value):
            return "Unknown"

        return value

    if pd.isna(value):
        return "Unknown"

    return value


# ============================================================
# 5. COMPLETE STAR LOOKUP
# ============================================================

def lookup_star(kic_id):

    print("\nLooking up KIC:", kic_id)

    nasa_data = get_nasa_stellar_data(kic_id)

    oxygen = get_oxygen(kic_id)

    star_data = {

        "KIC ID": int(kic_id),

        "Oxygen": oxygen,

        "Metallicity": nasa_data["Metallicity"],

        "Radius": nasa_data["Radius"],

        "Distance": nasa_data["Distance"]

    }

    return star_data


# ============================================================
# 6. ASTROSAGE
# ============================================================

def ask_astrosage(kic_id):

    # --------------------------------------------------------
    # FIRST: get verified catalog data
    # --------------------------------------------------------

    star_data = lookup_star(kic_id)


    # --------------------------------------------------------
    # SECOND: construct a prompt containing the actual data
    # --------------------------------------------------------

    prompt = f"""
You are AstroSage, an astronomy AI assistant.

You have been given verified stellar catalog data.

Do NOT search your own memory for these values.
Do NOT invent or estimate missing values.
Do NOT change any numerical value supplied below.

KIC ID:
{kic_id}

Verified stellar data:

Oxygen abundance [O/H]:
{star_data["Oxygen"]}

Metallicity [Fe/H]:
{star_data["Metallicity"]}

Stellar Radius:
{star_data["Radius"]} solar radii

Distance:
{star_data["Distance"]} parsecs


TASK:

Return exactly these four values.

Use exactly this format:

- Oxygen: ...
- Metallicity: ...
- Radius: ...
- Distance: ...

If a value is "Unknown", output "Unknown".

Do not add any other text.
"""


    # --------------------------------------------------------
    # THIRD: ask AstroSage
    # --------------------------------------------------------

    result = generator(
        prompt,
        max_new_tokens=150,
        temperature=0.1,
        do_sample=False,
        return_full_text=False
    )


    answer = result[0]["generated_text"].strip()

    return answer, star_data


# ============================================================
# 7. TERMINAL TEST
# ============================================================

print("=" * 65)
print("                 AstroSage KIC LOOKUP")
print("=" * 65)

print("Enter a KIC ID.")
print("Type 'exit' to quit.")
print("=" * 65)


while True:

    user_input = input("\nKIC ID: ").strip()


    if user_input.lower() == "exit":

        print("Exiting AstroSage...")

        break


    # --------------------------------------------------------
    # Validate KIC
    # --------------------------------------------------------

    try:

        kic_id = int(user_input)

    except ValueError:

        print("Please enter a valid numeric KIC ID.")

        continue


    # --------------------------------------------------------
    # Lookup + AstroSage
    # --------------------------------------------------------

    answer, raw_data = ask_astrosage(kic_id)


    print("\nAstroSage:")
    print(answer)


    # --------------------------------------------------------
    # Optional debugging
    # --------------------------------------------------------

    print("\n[Retrieved catalog data]")
    print(raw_data)