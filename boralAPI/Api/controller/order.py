from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from Domain.Entities.user import User
# from Domain.Entities.order import Order
from Domain.Handlers.user import UserHandler

order_router = InferringRouter()

from pydantic import BaseModel
class Order(BaseModel):
    User: str
    Order: float
    PreviousOrder: bool


@cbv(order_router)
class OrderRoute():

    order: Order
    current_user: User = Depends(UserHandler.get_current_active_user)

    @order_router.post("/order", tags=['Order'])
    async def show_order(self):
        try:
            print("User: {}".format(self.current_user))
            return self.order
        except Exception as e:
            return JSONResponse(
                status_code=422,
                content={"Unable to return given data.\n Error: {}".format(e.__dict__)},
            )
