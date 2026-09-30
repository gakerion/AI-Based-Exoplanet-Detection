import csv
import random
import main
import helper

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

text = main.get_star_summary(str(id))


@app.get("/planetSelection")
def getData():

    print("Running HI")

    kpids = random.sample(
        [
            row["kepid"]
            for row in csv.DictReader(open("exo_predict.csv"))
            if row["koi_disposition"] in ("CONFIRMED", "FALSE POSITIVE")
        ],
        5
    )

    print("Selected KIC IDs:", kpids)

    return [kpids]


@app.post("/planetDetails")
def get_planet(id: int):
    
    print("HELLOOO")
    return{
        "kic_id": id,
        "star_data":helper.lookup_star(id),
        "composition_text":text
    }
