import requests
import pandas as pd
import io
import torch



# ============================================================
# 2. NASA EXOPLANET ARCHIVE
# ============================================================

NASA_TAP_URL = (
    "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
)


def get_nasa_stellar_data(kic_id):

    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

    query = f"""
        SELECT
            kepid,
            mass,
            logg,
            radius,
            dist
        FROM keplerstellar
        WHERE kepid = {int(kic_id)}
    """

    params = {
        "query": query,
        "format": "json"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        if len(data) < 4:
            return {
                "Mass": "Unknown",
                "Gravity": "Unknown",
                "Radius": "Unknown",
                "Distance": "Unknown"
            }

        # ---------------------------------------------
        # 3rd record → Mass, Gravity, Radius
        # ---------------------------------------------

        row_3 = data[2]

        # ---------------------------------------------
        # 4th record → Distance
        # ---------------------------------------------

        row_4 = data[3]

        return {
            "Mass": clean_value(row_3.get("mass")),
            "Gravity": clean_value(row_3.get("logg")),
            "Radius": clean_value(row_3.get("radius")),
            "Distance": clean_value(row_4.get("dist"))
        }

    except Exception as e:

        print("NASA lookup error:", e)

        return {
            "Mass": "Unknown",
            "Gravity": "Unknown",
            "Radius": "Unknown",
            "Distance": "Unknown"
        }
# ============================================================
# 3. VIZIER OXYGEN CATALOG
# ============================================================

VIZIER_FIELD_URL = (
    "https://cdsarc.cds.unistra.fr/ftp/cats/J/A+A/594/A43/field.dat"
)
VIZIER_URL = "https://vizier.cds.unistra.fr/viz-bin/asu-tsv"

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

    url = "https://vizier.cds.unistra.fr/viz-bin/asu-tsv"

    params = {
        "-source": "J/A+A/594/A43/field",
        "KIC": f"={int(kic_id)}",
        "-out": "KIC,[O/H]",
        "-out.max": "1"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        lines = response.text.splitlines()

        # Find the actual data row.
        for line in lines:

            line = line.strip()

            # Skip comments, headers, separators and empty lines
            if (
                not line
                or line.startswith("#")
                or line.startswith("KIC")
                or line.startswith("-")
            ):
                continue

            parts = line.split()

            # Expected:
            # 10907196 -0.16
            if len(parts) >= 2:

                returned_kic = parts[0]
                oxygen = parts[1]

                if returned_kic == str(int(kic_id)):

                    try:
                        return float(oxygen)
                    except ValueError:
                        return "Unknown"

        return "Unknown"

    except Exception as e:
        print("VizieR oxygen lookup error:", e)
        return "Unknown"
    
def get_hydrogen(kic_id):
    """
    Look up hydrogen for a KIC ID.

    NASA's keplerstellar catalog does not contain
    a direct hydrogen abundance/mass-fraction column.

    Therefore, if no direct database value is available,
    return Unknown. No estimation is performed.
    """

    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

    query = f"""
        SELECT kepid
        FROM keplerstellar
        WHERE kepid = {int(kic_id)}
    """

    params = {
        "query": query,
        "format": "json"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        if not data:
            return "Unknown"

        # The catalog has no direct hydrogen field.
        return "Unknown"

    except Exception as e:
        print("Hydrogen lookup error:", e)
        return "Unknown"


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

    nasa_data = get_nasa_stellar_data(kic_id)

    oxygen = get_oxygen(kic_id)

    hydrogen = get_hydrogen(kic_id)

    return {
        "Oxygen": oxygen,
        "Metallicity": "Unknown",
        "Mass": nasa_data["Mass"],
        "Gravity": nasa_data["Gravity"],
        "Radius": nasa_data["Radius"],
        "Distance": nasa_data["Distance"],
        "Hydrogen": hydrogen
    }
    return star_data


# ============================================================
# 6. ASTROSAGE
# ============================================================

def get_star_info(kic_id):

    star_data = lookup_star(kic_id)

    return (
        f"- Oxygen: {star_data['Oxygen']}\n"
        f"- Metallicity: {star_data['Metallicity']}\n"
        f"- Mass: {star_data['Mass']}\n"
        f"- Gravity: {star_data['Gravity']}\n"
        f"- Radius: {star_data['Radius']}\n"
        f"- Distance: {star_data['Distance']}\n"
        f"- Hydrogen: {star_data['Hydrogen']}"
    )


while True:
    user_input = input("\nKIC ID: ").strip()

    if user_input.lower() == "exit":
        print("Exiting AstroSage...")
        break

    try:
        kic_id = int(user_input)
    except ValueError:
        print("Please enter a valid numeric KIC ID.")
        continue

    answer = get_star_info(kic_id)

    print("\nAstroSage:")
    print(answer)

