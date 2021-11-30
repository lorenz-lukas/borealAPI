from fastapi import FastAPI
from pydantic import BaseModel
from requests import get
from json import loads


class Order(BaseModel):
    User: str
    Order: float
    PreviousOrder: bool


app = FastAPI()


@app.get("/openBreweriesAll")
async def root():
    try:
        res = get("https://api.openbrewerydb.org/breweries/")
        openBreweriesApiResult = res.__dict__
        return loads(openBreweriesApiResult["_content"])
    except:
        return "Unable to retrieve data from https://api.openbrewerydb.org/breweries/.", 400


@app.get("/openBreweriesNames")
async def root():
    try:
        res = get("https://api.openbrewerydb.org/breweries/")
        openBreweriesApiResult = res.__dict__
        names = [beer["name"] for beer in loads(openBreweriesApiResult["_content"])]
        return names
    except:
        return "Unable to retrieve data from https://api.openbrewerydb.org/breweries/.", 400


@app.post("/order")
async def show_order(order: Order):
    return order