import csv
import random

from test import lookup_star
import main
import helper
from fastapi import FastAPI

app = FastAPI()


@app.get("/explore")
def getData():
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
    return {"kpids": helper.get_random_kpids("kepler_data.csv")}