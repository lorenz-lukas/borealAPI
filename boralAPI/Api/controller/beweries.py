from json import loads
from requests import get
from fastapi.responses import JSONResponse
from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from Domain.Entities.user import User
from Domain.Handlers.user import UserHandler


beweries_router = InferringRouter()


@cbv(beweries_router)
class Beweries():

    current_user: User = Depends(UserHandler.get_current_active_user)

    @beweries_router.get("/getAll", tags=['Open Breweries'])
    async def get_all_breweries_data(self):
        try:
            print("User: {}".format(self.current_user))
            res = get("https://api.openbrewerydb.org/breweries/")
            openBreweriesApiResult = res.__dict__
            return loads(openBreweriesApiResult["_content"])
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"Unable to retrieve data from https://api.openbrewerydb.org/breweries/.\n Error: {}".format(e.__dict__)},
            )


    @beweries_router.get("/getNames", tags=['Open Breweries'])
    async def get_breweries_name(self):
        try:
            print("User: {}".format(self.current_user))
            res = get("https://api.openbrewerydb.org/breweries/")
            openBreweriesApiResult = res.__dict__
            names = [beer["name"] for beer in loads(openBreweriesApiResult["_content"])]
            return names
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"Unable to retrieve data from https://api.openbrewerydb.org/breweries/.\n Error: {}".format(e.__dict__)},
            )