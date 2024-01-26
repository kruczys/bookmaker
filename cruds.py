from datetime import datetime
from random import randint
from typing import List

from bson import ObjectId
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.openapi.models import Response
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument
from starlette import status

from models import UserBet, Comment, Bet, User

client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client.bookmaker
users_collection = db.get_collection("users")
bets_collection = db.get_collection("bets")
user_bets_collection = db.get_collection("user_bets")
comments_collection = db.get_collection("comments")


async def get_all_users() -> List[User]:
    users = await users_collection.find().to_list(length=1000)
    return users


async def create_user(user: User):
    new_user = await users_collection.insert_one(
        user.model_dump(by_alias=True, exclude=["id"])
    )
    created_user = await users_collection.find_one(
        {"_id": new_user.inserted_id}
    )
    return created_user


async def update_user_balance(user_id: str, amount: float, operation: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id: {user_id} not found")
    if operation == "increase":
        new_balance = user.get('balance', 0) + amount
    elif operation == "decrease":
        new_balance = user.get('balance', 0) - amount
    else:
        raise HTTPException(status_code=401, detail=f"Invalid operation: {operation}")
    user = await users_collection.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": {"balance": new_balance}},
        return_document=ReturnDocument.AFTER)
    return {"success": True}


async def create_bet(bet: Bet):
    bet.result = randint(0, 2)
    new_bet = await bets_collection.insert_one(
        bet.model_dump(by_alias=True, exclude=["id"])
    )
    created_bet = await bets_collection.find_one(
        {"_id": new_bet.inserted_id}
    )
    return created_bet


async def get_resolved_bets():
    current_time = datetime.now()
    resolved_bets = db.bets.find({"resolve_date": {"$lte": current_time}})
    return await resolved_bets.to_list(length=100)


async def create_user_bet(user_bet: UserBet):
    user_bet_doc = jsonable_encoder(user_bet)
    await db.user_bets.insert_one(user_bet_doc)


async def resolve_user_bet(user_bet_id: str):
    await db.user_bets.update_one({"id": user_bet_id}, {"$set": {"resolved": True}})


async def create_comment(comment: Comment):
    comment_doc = jsonable_encoder(comment)
    await db.comments.insert_one(comment_doc)


async def get_user_by_id(id: str):
    if (
            user := await users_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return user

    raise HTTPException(status_code=404, detail=f"User with id: {id} not found")


async def get_bet_by_id(bet_id: str):
    return await db.bets.find_one({"id": bet_id})


async def get_user_bet_by_id(user_bet_id: str):
    return await db.user_bets.find_one({"id": user_bet_id})


async def get_comments_by_bet_id(bet_id: str):
    comments = db.comments.find({"bet_id": bet_id})
    return await comments.to_list(length=100)


async def update_bet(bet_id: str, update_data: dict):
    await db.bets.update_one({"id": bet_id}, {"$set": update_data})


async def update_comment(comment_id: str, new_text: str):
    await db.comments.update_one({"id": comment_id}, {"$set": {"text": new_text}})


async def delete_user(id: str):
    delete_result = await users_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT, description=f"User with id: {id} deleted")

    raise HTTPException(status_code=404, detail=f"User with id: {id} not found")


async def delete_bet(bet_id: str):
    await db.bets.delete_one({"id": bet_id})


async def delete_user_bet(user_bet_id: str):
    await db.user_bets.delete_one({"id": user_bet_id})


async def delete_comment(comment_id: str):
    await db.comments.delete_one({"id": comment_id})


class BetManager:
    def __init__(self, client):
        self.client = client

    async def resolve_bets(self):
        resolved_bets = await get_resolved_bets()
        for bet in resolved_bets:
            user_bets = await db.user_bets.find({"bet_id": bet['id'], "resolved": False})
            for user_bet in user_bets:
                if bet['result'] == user_bet['option']:
                    await update_user_balance(user_bet['user_id'], user_bet['amount'] * 1.67, "increase")
                await resolve_user_bet(user_bet['id'])
                self.client.publish("bets/resolved", f"{bet['title']} just got resolved")
