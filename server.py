import csv
import random
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


@app.get("/explore")
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