from main import client
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List


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

    def get_ranking_dict(self):
        return {
            "username": self.username,
            "balance": self.balance
        }


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
    amount: float
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
        if len(bets) > 0:
            user_bets_copy = self.user_bets[:]
            for user_bet in user_bets_copy:
                if self.bets[str(user_bet.bet_id)].is_resolved():
                    message = f"{bets[user_bet.bet_id].title} just got resolved"
                    client.publish("bets/resolved", message)
                    user_bet.resolve()
                    if self.bets[str(user_bet.bet_id)].result == user_bet.option:
                        self.users[str(user_bet.user_id)].increase_balance(user_bet.amount * 1.67)
                    self.user_bets.remove(user_bet)
        else:
            return {"message": "No bets in database"}
