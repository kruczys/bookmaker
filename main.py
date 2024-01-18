import paho.mqtt.client as mqtt

from datetime import datetime
from typing import List, Dict
from uuid import uuid4

from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

app = FastAPI()

client = mqtt.Client()
client.connect("mqtt.eclipse.org")
client.loop_start()


class User(BaseModel):
    username: str
    balance: float

    def reduce_balance(self, amount: float):
        if self.balance < amount:
            raise ValueError("Not enough money")
        else:
            self.balance -= amount

    def increase_balance(self, amount: float):
        if self.balance >= 0:
            self.balance += amount
        else:
            raise ValueError("Amount cannot be below 0")


class Bet(BaseModel):
    creator_username: str
    title: str
    resolve_date: datetime
    result: int

    def is_resolved(self):
        return self.resolve_date <= datetime.now()


class UserBet(BaseModel):
    user_id: str
    bet_id: str
    amount: int
    option: int
    resolved: bool = False

    def resolve(self):
        if self.resolved:
            raise ValueError("Bet already resolved")
        else:
            self.resolved = True


class Comment(BaseModel):
    bet_id: str
    creator_username: str
    text: str
    create_date: datetime
    likes: int

    def increment_likes(self):
        self.likes += 1


class BetManager:
    users: Dict[str, User]
    user_bets: List[UserBet]
    bets: Dict[str, Bet]

    def __init__(self, users: Dict[str, User], user_bets: List[UserBet], bets: Dict[str, Bet]):
        self.users = users
        self.user_bets = user_bets
        self.bets = bets

    def resolve_bets(self):
        user_bets_copy = self.user_bets[:]
        for user_bet in user_bets_copy:
            if self.bets[str(user_bet.bet_id)].is_resolved():
                message = f"{bets[user_bet.bet_id].title} just got resolved"
                client.publish("bets/resolved", message)
                user_bet.resolve()
                if self.bets[str(user_bet.bet_id)].result == user_bet.option:
                    self.users[str(user_bet.user_id)].increase_balance(user_bet.amount * 1.67)
                self.user_bets.remove(user_bet)


users = {}
usernames = []
bets = {}
comments = []
user_bets = []
bet_manager = BetManager(users=users, user_bets=user_bets, bets=bets)


@app.post("/auth/signup")
async def create_user(user: User):
    user_id = str(uuid4())
    if user.username not in usernames:
        users[user_id] = user
        usernames.append(user.username)
        return {"message": "User created successfully"}
    else:
        return {"message": "User already exists"}


@app.delete("/auth/delete/{username}")
async def delete_user(username: str):
    if username in usernames:
        user_id_info = await get_user_id(username)
        user_id = user_id_info["user_id"]
        del users[user_id]
        usernames.remove(username)
        return {"message": "User deleted successfully"}
    return HTTPException(status_code=404, detail="User does not exist")


@app.put("/auth/update_username/{username}")
async def update_username(username: str, new_username: str):
    if new_username not in usernames:
        usernames.remove(username)
        user_id_info = await get_user_id(username)
        user_id = user_id_info["user_id"]
        users[user_id].username = new_username
        usernames.append(new_username)
        return {"message": "Username updated successfully"}
    return {"message": "Username already in database"}


@app.get("/auth/user_id/{username}")
async def get_user_id(username: str):
    for user_id, user_data in users.items():
        if user_data.username == username:
            return {"user_id": user_id}
    raise HTTPException(status_code=404, detail="User not found")


@app.get("/bet")
async def get_bets():
    return {"bets": bets}


@app.get("/bet/{substring}")
async def get_bets_by_title(substring: str):
    query = [bet for bet_id, bet in bets.items() if substring in bet.title]
    if query:
        return {"bets": query}
    return HTTPException(status_code=404, detail="Bets not found")


@app.post("/bet")
async def create_bet(bet: Bet):
    bet_id = str(uuid4())
    bets[bet_id] = bet
    return {"message": "Bet created successfully"}


@app.get("/bet/bet_id/{title}")
async def get_bet_id(title: str):
    for bet_id, bet_data in bets.items():
        if bet_data.title == title:
            return {"bet_id": bet_id}
    raise HTTPException(status_code=404, detail="Bet not found")


@app.put("/bet/{title}")
async def update_bet(bet: Bet, title: str, creator_username: str):
    bet_id_info = await get_bet_id(title)
    bet_id = bet_id_info["bet_id"]
    if bet_id and bets[bet_id].creator_username == creator_username:
        bets[bet_id] = bet
        return {"message": "Bets updated successfully"}
    return HTTPException(status_code=404, detail="Bet not found or user is not creator")


@app.delete("/bet/{title}")
async def delete_bet(title: str, creator_username: str):
    bet_id_info = await get_bet_id(title)
    bet_id = bet_id_info["bet_id"]
    if bet_id and bets[bet_id].creator_username == creator_username:
        del bets[bet_id]
        return {"message": "Bet deleted successfully"}
    return HTTPException(status_code=404, detail="Bet not found or user is not creator")


@app.get("/user_bets/{user_id}")
async def get_user_bets(user_id: str):
    if user_id in users:
        query = [user_bet for user_bet in user_bets if user_bet.user_id == user_id]
        return {"user_bets": query}
    return HTTPException(status_code=404, detail="User not found")


def is_valid_user_bet(user_bet: UserBet) -> bool:
    return (
            user_bet.bet_id in bets
            and user_bet.user_id in users
            and user_bet.amount > 0
            and user_bet.option in [0, 1, 2]
            and not bets[user_bet.bet_id].is_resolved()
    )


@app.post("/user_bets")
async def create_user_bet(user_bet: UserBet):
    if is_valid_user_bet(user_bet):
        users[user_bet.user_id].reduce_balance(user_bet.amount)
        user_bets.append(user_bet)
        return {"message": "User's bet created successfully"}
    return HTTPException(status_code=404, detail="User's bet not found")


@app.delete("/user_bets")
async def delete_user_bet(user_bet: UserBet):
    if is_valid_user_bet(user_bet):
        users[user_bet.user_id].increase_balance(user_bet.amount)
        user_bet.remove(user_bet)
        return {"message": "User's bet deleted successfully"}
    return HTTPException(status_code=404, detail="User's bet not found")


@app.post("/comment")
async def create_comment(comment: Comment):
    if comment.creator_username in usernames:
        comments.append(comment)
        return {"message": "Comment created successfully"}
    return HTTPException(status_code=404, detail="User not found")


@app.get("/comments")
async def get_comments():
    return {"comments": comments}


@app.get("comments/{username_substring}")
async def get_comments_by_username(username_substring: str):
    query = [comment for comment in comments if username_substring in comment.creator_username]
    if query:
        return {"comments": query}
    return HTTPException(status_code=404, detail="User not found")


@app.put("comments/{bet_id}/{username}")
async def update_comment(comment: Comment, bet_id: int, username: str):
    if bet_id in bets and username in usernames:
        for com in comments:
            if com.bet_id == bet_id and com.username == username:
                com.text = comment.text
                return {"message": "Comment updated successfully"}
    return HTTPException(status_code=404, detail="No bet or username found")


@app.delete("comments/{bet_id}/{username}")
async def delete_comment(bet_id: int, username: str):
    if bet_id in bets and username in usernames:
        for comment in comments:
            if comment.bet_id == bet_id and comment.creator_username == username:
                comments.remove(comment)
                return {"message": "Comment deleted successfully"}
    return HTTPException(status_code=404, detail="No bet or username found")
