from datetime import datetime
from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    username: str
    balance: int


class Bet(BaseModel):
    creator_username: str
    title: str
    resolve_date: datetime
    result: int
    win_amount_wagered: int
    draw_amount_wagered: int
    loose_amount_wagered: int
    total_amount_wagered: int


class UserBet(BaseModel):
    user_id: int
    bet_id: int
    amount: int
    option: int


class Comment(BaseModel):
    id: int
    owner_username: str
    create_date: datetime


users = {}
usernames = []
bets = {}
comments = []
user_bets = []


@app.post("/auth/signup")
async def create_user(user: User):
    user_id = str(uuid4())
    if user.username not in usernames:
        users[user_id] = user
        usernames.append(user.username)
        return {"message": "User created successfully"}
    else:
        return {"message": "User already exists"}


@app.delete('/auth/delete')
async def delete_user(user: User, user_id: str):
    del users[user_id]
    usernames.remove(user.username)


@app.put("/auth/update_username")
async def update_username(user_id: str, new_username: str):
    users[user_id].username = new_username
    return {"message": "Username updated successfully"}


@app.get("/auth/user_id")
async def get_user_id(user: User):
    for user_id, user_data in users.items():
        if user_data.username == user.username:
            return {"user_id": user_id}
    return {"message": "User not found"}


@app.get("/bet")
async def get_bets():
    return {"bets": bets}


@app.post("/bet")
async def create_bet(bet: Bet):
    bet_id = str(uuid4())
    bets[bet_id] = bet
    return {"message": "Bet created successfully"}


@app.put("/bet")
async def update_bet(bet: Bet, bet_id: str, username: str):
    if bet_id in bets and bets[bet_id].username == username:
        bets[bet_id] = bet
        return {"message": "Bet updated successfully"}
    return {"message": "Bet not found"}


@app.delete("/bet")
async def delete_bet(bet_id: str):
    del bets[bet_id]
    return {"message": "Bet deleted successfully"}


@app.get("/user_bets")
async def get_user_bets(user_id: str):
    query = []
    if user_id in users:
        for user_bet in user_bets:
            if user_bet.user_id == user_id:
                query.append(user_bet)
        return {"user_bets": query}
    return {"message": "User not found"}


@app.post("/user_bets")
async def create_user_bet(user_bet: UserBet):
    if user_bet.bet_id in bets and user_bet.user_id in users and user_bet.amount > 0 and user_bet.option in [0, 1, 2]:
        user_bets.append(user_bet)
        return {"message": "User's bet created successfully"}
    return {"message": "User or bet not found or amount or option not valid"}


@app.put("/user_bets")
async def update_user_bets(user_bet: UserBet):
    if user_bet in user_bets:
        index = user_bets.index(user_bet)
        user_bets[index] = user_bet
        return {"message": "User's bet updated successfully"}
    return {"message": "User's bet not found"}
