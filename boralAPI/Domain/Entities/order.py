from pydantic import BaseModel


class Order(BaseModel):
    User: str
    Order: float
    PreviousOrder: bool