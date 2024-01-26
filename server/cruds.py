import json
from datetime import datetime
from random import randint
from typing import List
import paho.mqtt.client as mqtt
from bson import ObjectId
from fastapi import HTTPException
from fastapi.openapi.models import Response
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument
from starlette import status

from models import UserBet, Comment, Bet, User


db_client = AsyncIOMotorClient('mongodb://localhost:27017')
db = db_client.bookmaker
users_collection = db.get_collection("users")
bets_collection = db.get_collection("bets")
user_bets_collection = db.get_collection("user_bets")
comments_collection = db.get_collection("comments")


async def get_all_users() -> List[User]:
    users = await users_collection.find().to_list(length=1000)
    return users


async def create_user(user: User) -> User:
    new_user = await users_collection.insert_one(
        user.model_dump(by_alias=True, exclude=["id"])
    )
    created_user = await users_collection.find_one(
        {"_id": new_user.inserted_id}
    )
    return created_user


async def update_user_balance(user_id: str, amount: float, operation: str) -> User:
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
    return user


async def create_bet(bet: Bet) -> Bet:
    bet.result = randint(0, 2)
    new_bet = await bets_collection.insert_one(
        bet.model_dump(by_alias=True, exclude=["id"])
    )
    created_bet = await bets_collection.find_one(
        {"_id": new_bet.inserted_id}
    )
    return created_bet


async def get_resolved_bets() -> List[Bet]:
    current_time = datetime.now()
    resolved_bets = bets_collection.find({"resolve_date": {"$lt": current_time}})
    return resolved_bets


async def get_unresolved_bets() -> List[Bet]:
    current_time = datetime.now()
    resolved_bets = bets_collection.find({"resolve_date": {"$gt": current_time}})
    return resolved_bets


async def create_user_bet(user_bet: UserBet):
    new_user_bet = await users_collection.insert_one(
        user_bet.model_dump(by_alias=True, exclude=["id"])
    )
    created_user_bet = await users_collection.find_one(
        {"_id": new_user_bet.inserted_id}
    )
    return created_user_bet


async def resolve_user_bet(user_bet_id: str):
    await user_bets_collection.update_one({"_id": user_bet_id}, {"$set": {"resolved": True}})


async def create_comment(comment: Comment):
    new_comment = await comments_collection.insert_one(
        comment.model_dump(by_alias=True, exclude=["id"])
    )
    created_comment = await comments_collection.find_one(
        {"_id": new_comment.inserted_id}
    )
    return created_comment


async def get_user_by_id(id: str) -> User:
    if (
            user := await users_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return user

    raise HTTPException(status_code=404, detail=f"User with id: {id} not found")


async def get_bet_by_id(id: str) -> Bet:
    if (
            bet := await bets_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return bet

    raise HTTPException(status_code=404, detail=f"Bet with id: {id} not found")


async def get_user_bet_by_id(id: str) -> UserBet:
    if (
            user_bet := await users_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return user_bet

    raise HTTPException(status_code=404, detail=f"User with id: {id} not found")


async def get_comments_by_bet_id(id: str) -> Comment:
    if (
            comment := await comments_collection.find_one({"bet_id": ObjectId(id)})
    ) is not None:
        return comment

    raise HTTPException(status_code=404, detail=f"Comment with bet id: {id} not found")


async def get_comment_by_id(id: str) -> Comment:
    if (
            comment := await comments_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return comment

    raise HTTPException(status_code=404, detail=f"Comment with id: {id} not found")


async def update_bet_title(bet_id: str, new_title: str) -> Bet:
    bet = await get_bet_by_id(bet_id)
    if bet is not None:
        updated_bet = await bets_collection.find_one_and_update(
            {"_id": ObjectId(bet_id)},
            {"$set": {"title": new_title}},
            return_document=ReturnDocument.AFTER
        )
        return updated_bet
    return bet


async def update_comment_text(comment_id: str, new_text: str) -> Comment:
    comment = await get_comment_by_id(comment_id)
    if comment is not None:
        updated_comment = await comments_collection.find_one_and_update(
            {"_id": ObjectId(comment_id)},
            {"$set": {"text": new_text}},
            return_document=ReturnDocument.AFTER
        )
        return updated_comment
    return comment


async def delete_user(id: str):
    delete_result = await users_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT, description=f"User with id: {id} deleted")

    raise HTTPException(status_code=404, detail=f"User with id: {id} not found")


async def delete_bet(id: str):
    delete_result = await bets_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT, description=f"Bet with id: {id} deleted")

    raise HTTPException(status_code=404, detail=f"Bet with id: {id} not found")


async def delete_user_bet(id: str):
    delete_result = await user_bets_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT, description=f"User bet with id: {id} deleted")

    raise HTTPException(status_code=404, detail=f"User with id: {id} not found")


async def delete_comment(id: str):
    delete_result = await comments_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT, description=f"Comment with id: {id} deleted")



