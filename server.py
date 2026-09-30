import csv
import random
import main
import helper

import helper
import main

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

text = main.get_star_summary(str(id))


# ============================================================
# INITIALIZE ASTROSAGE ON SERVER START
# ============================================================

@app.on_event("startup")
def load_model():
    threading.Thread(target=main.initialize_astrosage, daemon=True).start()

# ============================================================
# PLANET SELECTION
# ============================================================

@app.get("/planetSelection")
def getData():

    print("Running /planetSelection")

    selected = random.sample(
        [
            row["kepid"]
            for row in csv.DictReader(
                open("exo_predict.csv")
            )
            if row["koi_disposition"] in (
                "CONFIRMED",
                "FALSE POSITIVE"
            )
        ],
        5
    )

    return selected


# ============================================================
# PLANET DETAILS
# ============================================================

@app.get("/planetDetails")
def get_planet(id: str):

    print(f"Getting details for KIC {id}")

    text = main.get_star_summary(id)

    return {
        "kic_id": id,
        "star_data": helper.lookup_star(id),
        "composition_text": text
    }
