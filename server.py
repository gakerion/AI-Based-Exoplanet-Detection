from test import lookup_star
from fastapi import FastAPI

app = FastAPI()

@app.get("/explore")
def getData():
    return{
        lookup_star()
    }