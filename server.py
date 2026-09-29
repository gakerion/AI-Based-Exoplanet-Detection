from test import lookup_star
import main
from fastapi import FastAPI

app = FastAPI()

@app.get("/explore")
def getData():
    return{
        main.get_random_kpids("exo_predict.csv")
    }