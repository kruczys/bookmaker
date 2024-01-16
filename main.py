from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    password: str
    balance: int


class Bet(BaseModel):
    id: int
    title: str
    resolve_date: datetime
    result: int


class UserBet(BaseModel):
    user: User
    bet: Bet
    amount: int
    option: int


class Comment(BaseModel):
    id: int
    owner: User
    create_date: datetime


users = []
bets = []
comments = []
user_bets = []

