import csv
import random

import pandas as pd
import requests

NASA_TAP_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
VIZIER_URL = "https://vizier.cds.unistra.fr/viz-bin/asu-tsv"


def get_nasa_stellar_data(kic_id):
    """Get stellar data for one KIC ID from NASA Exoplanet Archive."""
    query = f"""
        SELECT kepid, mass, logg, radius, dist
        FROM keplerstellar
        WHERE kepid = {int(kic_id)}
    """

    params = {"query": query, "format": "json"}

    try:
        response = requests.get(NASA_TAP_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        if not data:
            return {
                "Mass": "Unknown",
                "Gravity": "Unknown",
                "Radius": "Unknown",
                "Distance": "Unknown",
            }

        # The query is for one KIC, so use the returned row directly.
        row = data[0]

        return {
            "Mass": clean_value(row.get("mass")),
            "Gravity": clean_value(row.get("logg")),
            "Radius": clean_value(row.get("radius")),
            "Distance": clean_value(row.get("dist")),
        }

    except Exception as e:
        print("NASA lookup error:", e)
        return {
            "Mass": "Unknown",
            "Gravity": "Unknown",
            "Radius": "Unknown",
            "Distance": "Unknown",
        }


def get_oxygen(kic_id):
    """Get oxygen abundance [O/H] from the VizieR catalog."""
    params = {
        "-source": "J/A+A/594/A43/field",
        "KIC": f"={int(kic_id)}",
        "-out": "KIC,[O/H]",
        "-out.max": "1",
    }

    try:
        response = requests.get(VIZIER_URL, params=params, timeout=30)
        response.raise_for_status()

        for line in response.text.splitlines():
            line = line.strip()

            if (
                not line
                or line.startswith("#")
                or line.startswith("KIC")
                or line.startswith("-")
            ):
                continue

            parts = line.split()

            if len(parts) >= 2 and parts[0] == str(int(kic_id)):
                try:
                    return float(parts[1])
                except ValueError:
                    return "Unknown"

        return "Unknown"

    except Exception as e:
        print("VizieR oxygen lookup error:", e)
        return "Unknown"


def get_hydrogen(kic_id):
    """Return hydrogen abundance when a direct catalog value exists.

    The current NASA keplerstellar query used by this project has no
    hydrogen abundance field, so no estimate is made.
    """
    return "Unknown"


def clean_value(value):
    """Convert missing numeric/catalog values to 'Unknown'."""
    if value is None:
        return "Unknown"

    try:
        if pd.isna(value):
            return "Unknown"
    except (TypeError, ValueError):
        pass

    return value


def logg_to_ms2(logg):
    """Convert log10 surface gravity in cgs to m/s²."""
    if logg == "Unknown":
        return "Unknown"

    try:
        gravity_cgs = 10 ** float(logg)
        return gravity_cgs / 100
    except (TypeError, ValueError, OverflowError):
        return "Unknown"


def lookup_star(kic_id):
    """Collect all available catalog information for a KIC ID."""
    try:
        kic_id = int(kic_id)
    except (TypeError, ValueError):
        raise ValueError("KIC ID must be a number.")

    nasa_data = get_nasa_stellar_data(kic_id)
    oxygen = get_oxygen(kic_id)
    hydrogen = get_hydrogen(kic_id)
    gravity = logg_to_ms2(nasa_data["Gravity"])

    if gravity != "Unknown":
        gravity = round(gravity, 2)

    distance = nasa_data["Distance"]
    if distance != "Unknown":
        try:
            distance = float(distance) * 3.26
            distance = round(distance, 2)
        except (TypeError, ValueError):
            distance = "Unknown"

    return {
        "Oxygen": oxygen,
        "Metallicity": "Unknown",
        "Mass": nasa_data["Mass"],
        "Gravity": gravity,
        "Radius": nasa_data["Radius"],
        "Distance": distance,
        "Hydrogen": hydrogen,
    }


def get_star_info(kic_id):
    """Return star data as text for use in an AI prompt."""
    star_data = lookup_star(kic_id)

    return (
        f"- Oxygen: {star_data['Oxygen']}\n"
        f"- Metallicity: {star_data['Metallicity']}\n"
        f"- Mass: {star_data['Mass']} solar masses\n"
        f"- Gravity: {star_data['Gravity']} m/s²\n"
        f"- Radius: {star_data['Radius']} solar radii\n"
        f"- Distance: {star_data['Distance']} light years\n"
        f"- Hydrogen: {star_data['Hydrogen']}"
    )


def get_random_kpids(filename):
    """Return 5 random KIC IDs, including one of each disposition."""
    confirmed = []
    false_positive = []

    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            kepid = row.get("kepid")
            disposition = row.get("koi_disposition")

            if not kepid:
                continue

            if disposition == "CONFIRMED":
                confirmed.append((kepid, disposition))
            elif disposition == "FALSE POSITIVE":
                false_positive.append((kepid, disposition))

    if not confirmed or not false_positive:
        raise ValueError(
            "The CSV must contain at least one CONFIRMED and one FALSE POSITIVE entry."
        )

    selected = [random.choice(confirmed), random.choice(false_positive)]
    selected_set = set(selected)

    remaining = [
        item for item in confirmed + false_positive
        if item not in selected_set
    ]

    if len(remaining) < 3:
        raise ValueError("The CSV must contain at least 5 usable entries.")

    selected.extend(random.sample(remaining, 3))
    random.shuffle(selected)

    return selected
