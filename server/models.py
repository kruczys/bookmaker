from datetime import datetime
from typing import Optional, Annotated

from pydantic import BaseModel, Field, BeforeValidator, ConfigDict

PyObjectId = Annotated[str, BeforeValidator(str)]


class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str
    password: str
    balance: float = 1000
    logged_in: bool = False
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "username": "John",
                "password": "john",
                "balance": 1000,
                "logged_in": False,
            }
        }
    )


class Bet(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    creator_username: str
    title: str
    resolve_date: datetime
    result: int = 0
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "creator_username": "John",
                "title": "john",
                "resolve_date": datetime(year=2077, month=12, day=12),
            }
        }
    )


class UserBet(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str
    bet_id: str
    amount: float
    option: int
    resolved: bool = False
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "user_id": "John",
                "bet_id": "bet_id",
                "amount": 100,
                "option": 1,
                "resolved": False,
            }
        }
    )


class Comment(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    bet_id: str
    creator_username: str
    text: str
    create_date: datetime
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "bet_id": "bet_id",
                "creator_username": "John",
                "text": "Lets go poland!",
                "create_date": datetime.now(),
            }
        }
    )
