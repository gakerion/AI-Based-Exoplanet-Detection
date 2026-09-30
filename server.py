import csv
import random
import helper
from main import get_star_summary
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



@app.get("/planetSelection")
def getData():
    print("Running HI")
    helper.get_random_kpids = lambda filename: tuple(
        random.sample(
            [
                row["kepid"]
                for row in csv.DictReader(open(filename))
                if row["koi_disposition"] in ("CONFIRMED", "FALSE POSITIVE")
            ],
            5,
        )
    )
    return [helper.get_random_kpids("exo_predict.csv")]




@app.get("/planetDetails")
def get_planet(id: str):

    text = get_star_summary(id)

    return{
        "kic_id": id,
        "star_data":helper.lookup_star(id),
        "composition_text":text
    }

