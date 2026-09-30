import csv
import random
from pathlib import Path

import helper
import main
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "exo_predict.csv"


@app.on_event("startup")
def startup():
    print("Starting AstroSage...")
    main.load_model()
    print("Server ready. AstroSage is loaded.")


@app.get("/planetSelection")
def get_data():
    """Return 5 random KIC IDs from confirmed/false-positive objects."""
    if not CSV_FILE.exists():
        raise HTTPException(
            status_code=500,
            detail=f"Could not find {CSV_FILE.name}"
        )

    with CSV_FILE.open("r", newline="", encoding="utf-8") as file:
        rows = csv.DictReader(file)
        valid_ids = [
            row["kepid"]
            for row in rows
            if row.get("kepid")
            and row.get("koi_disposition") in ("CONFIRMED", "FALSE POSITIVE")
        ]

    if len(valid_ids) < 5:
        raise HTTPException(
            status_code=500,
            detail="exo_predict.csv must contain at least 5 valid KIC IDs."
        )

    kpids = random.sample(valid_ids, 5)

    print("Selected KIC IDs:", kpids)
    return [kpids]


@app.get("/planetDetails")
@app.post("/planetDetails")
def get_planet(id: str):
    try:
        kic_id = int(id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=400,
            detail="KIC ID must be a number."
        )

    try:
        star_data = helper.lookup_star(kic_id)

        text = main.get_star_summary(kic_id)

        return {
            "kic_id": str(kic_id),
            "star_data": star_data,
            "composition_text": text
        }

    except Exception as e:
        print("Planet details error:", repr(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )