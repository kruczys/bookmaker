from datetime import datetime
from random import randint
from typing import List, Dict

import paho.mqtt.client as mqtt
from bson import ObjectId
from fastapi import HTTPException
from fastapi.openapi.models import Response
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReturnDocument
from starlette import status
from starlette.websockets import WebSocket

from server.models import UserBet, Comment, Bet, User

db_client = AsyncIOMotorClient('mongodb://localhost:27017')
db = db_client.bookmaker
users_collection = db.get_collection("users")
bets_collection = db.get_collection("bets")
user_bets_collection = db.get_collection("user_bets")
comments_collection = db.get_collection("comments")
connected_clients: Dict[str, WebSocket] = {}

mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883)


async def get_all_users() -> List[User]:
    users = await users_collection.find().to_list(length=1000)
    message = f"Got all users: {users}"
    mqtt_client.publish("logs", message)
    return users


async def create_user(user: User) -> User:
    user_dict = user.model_dump(by_alias=True, exclude=["id"])
    existing_user = await users_collection.find_one({"username": user_dict["username"]})
    if existing_user is not None:
        raise HTTPException(status_code=401, detail="User already exists")
    new_user = await users_collection.insert_one(
        user.model_dump(by_alias=True, exclude=["id"])
    )
    created_user = await users_collection.find_one(
        {"_id": new_user.inserted_id}
    )
    message = f"Created new user: {user}"
    mqtt_client.publish("logs", message)
    return created_user


async def broadcast_user_count() -> None:
    count = await users_collection.count_documents({"logged_in": True})
    message = {"user_count": count}
    for ws in connected_clients.values():
        await ws.send_json(message)


async def login_user(username: str, password: str) -> User:
    user = await users_collection.find_one({"username": username, "password": password})
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    await users_collection.update_one(
        {"username": user["username"]},
        {"$set": {"logged_in": True}},

    )
    user = await users_collection.find_one({"username": username, "password": password})
    message = f"Logged in user: {user}"
    mqtt_client.publish("logs", message)
    return user


async def count_users():
    count = await users_collection.count_documents({"logged_in": True})
    message = f"Counted users: {count}"
    mqtt_client.publish("logs", message)
    return count


async def logout_user(username: str) -> User:
    user = await users_collection.find_one({"username": username})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await users_collection.update_one(
        {"username": user["username"]},
        {"$set": {"logged_in": False}}
    )
    user = await users_collection.find_one({"username": username})
    message = f"Logged out user: {user}"
    mqtt_client.publish("logs", message)
    return user


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
    ws = connected_clients.get(user_id)
    if ws:
        await ws.send_json(user["balance"])
    message = f"Updated balance: {user}"
    mqtt_client.publish("logs", message)
    return user


async def create_bet(bet: Bet) -> Bet:
    bet.result = randint(0, 2)
    new_bet = await bets_collection.insert_one(
        bet.model_dump(by_alias=True, exclude=["id"])
    )
    created_bet = await bets_collection.find_one(
        {"_id": new_bet.inserted_id}
    )
    message = f"Created bet: {bet}"
    mqtt_client.publish("logs", message)
    return created_bet


async def get_resolved_bets() -> List[Bet]:
    current_time = datetime.now()
    resolved_bets = await bets_collection.find({"resolve_date": {"$lt": current_time}}).to_list(length=1000)
    message = f"Got resolved bets: {resolved_bets}"
    mqtt_client.publish("logs", message)
    return resolved_bets


async def search_resolved_bets(title_substring: str) -> List[Bet]:
    resolved_bets = await get_resolved_bets()
    matching_bets = [bet for bet in resolved_bets if title_substring in bet["title"]]
    message = f"Found {len(matching_bets)} resolved bets matching title substring: {title_substring}"
    mqtt_client.publish("logs", message)
    return matching_bets


async def get_unresolved_bets() -> List[Bet]:
    current_time = datetime.now()
    resolved_bets = await bets_collection.find({"resolve_date": {"$gt": current_time}}).to_list(length=1000)
    message = f"Got unresolved bets: {resolved_bets}"
    mqtt_client.publish("logs", message)
    return resolved_bets


async def get_all_bets() -> List[Bet]:
    bet = await bets_collection.find().to_list(length=1000)
    message = f"Got all bets: {bet}"
    mqtt_client.publish("logs", message)
    return bet


async def create_user_bet(user_bet: UserBet):
    user_bet_dict = user_bet.model_dump(by_alias=True, exclude=["id"])
    await update_user_balance(user_bet_dict["user_id"], user_bet_dict["amount"], "decrease")
    new_user_bet = await user_bets_collection.insert_one(
        user_bet.model_dump(by_alias=True, exclude=["id"])
    )
    created_user_bet = await user_bets_collection.find_one(
        {"_id": new_user_bet.inserted_id}
    )
    message = f"Created user bet: {new_user_bet}"
    mqtt_client.publish("logs", message)
    return created_user_bet


async def resolve_user_bet(user_bet_id: str):
    await user_bets_collection.update_one({"_id": user_bet_id}, {"$set": {"resolved": True}})
    message = f"Resolved user bet: {user_bet_id}"
    mqtt_client.publish("logs", message)


async def create_comment(comment: Comment):
    comment.create_date = datetime.now().isoformat()
    new_comment = await comments_collection.insert_one(
        comment.model_dump(by_alias=True, exclude=["id"])
    )
    created_comment = await comments_collection.find_one(
        {"_id": new_comment.inserted_id}
    )
    message = f"Created comment: {new_comment}"
    mqtt_client.publish("logs", message)
    return created_comment


async def get_user_by_id(id: str) -> User:
    if (
            user := await users_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        message = f"Got user by id: {user}"
        mqtt_client.publish("logs", message)
        return user

    raise HTTPException(status_code=404, detail=f"User with id: {id} not found")


async def get_bet_by_id(id: str) -> Bet:
    if (
            bet := await bets_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        message = f"Got bet by id: {bet}"
        mqtt_client.publish("logs", message)
        return bet

    raise HTTPException(status_code=404, detail=f"Bet with id: {id} not found")


async def get_all_user_bets(user_id: str) -> List[UserBet]:
    user_bets = await user_bets_collection.find({"user_id": user_id, "resolved": False}).to_list(length=1000)
    return user_bets


async def get_user_bet_by_id(id: str) -> UserBet:
    if (
            user_bet := await user_bets_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        message = f"Got user_bet by id: {user_bet}"
        mqtt_client.publish("logs", message)
        return user_bet

    raise HTTPException(status_code=404, detail=f"User bet with id: {id} not found")


async def get_comments_by_bet_id(id: str) -> List[Comment]:
    comments = await comments_collection.find({"bet_id": str(id)}).to_list(length=1000)
    message = f"Got comments by bet_id: {comments}"
    mqtt_client.publish("logs", message)
    return comments


async def get_comment_by_id(id: str) -> Comment:
    if (
            comment := await comments_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return comment

    raise HTTPException(status_code=404, detail=f"Comment with id: {id} not found")


async def update_password(user_id: str, old_password: str, new_password: str) -> User:
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if old_password != user["password"]:
        raise HTTPException(status_code=401, detail="Incorrect password")

    await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"password": new_password}}
    )

    updated_user = await users_collection.find_one({"_id": ObjectId(user_id)})
    message = f"Updated password: {user}"
    mqtt_client.publish("logs", message)
    return updated_user


async def update_bet_title(bet_id: str, new_title: str) -> Bet:
    bet = await get_bet_by_id(bet_id)
    if bet is not None:
        updated_bet = await bets_collection.find_one_and_update(
            {"_id": ObjectId(bet_id)},
            {"$set": {"title": new_title}},
            return_document=ReturnDocument.AFTER
        )
        message = f"Updated title: {bet}"
        mqtt_client.publish("logs", message)
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
        message = f"Updated text: {comment}"
        mqtt_client.publish("logs", message)
        return updated_comment
    return comment


async def delete_user(id: str):
    delete_result = await users_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        message = f"Deleted user: {id}"
        mqtt_client.publish("logs", message)
        return Response(status_code=status.HTTP_204_NO_CONTENT, description=f"User with id: {id} deleted")

    raise HTTPException(status_code=404, detail=f"User with id: {id} not found")


async def delete_bet(id: str, creator_username: str):
    bet = await bets_collection.find_one({"_id": ObjectId(id)})
    if bet['creator_username'] != creator_username:
        raise HTTPException(status_code=400, detail="User does not have permission to delete this bet")
    delete_result = await bets_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        message = f"Deleted bet: {id}"
        mqtt_client.publish("logs", message)
        return Response(status_code=status.HTTP_204_NO_CONTENT, description=f"Bet with id: {id} deleted")

    raise HTTPException(status_code=404, detail=f"Bet with id: {id} not found")


async def delete_user_bet(id: str):
    user_bet = await get_user_bet_by_id(id)
    delete_result = await user_bets_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        await update_user_balance(user_bet["user_id"], user_bet["amount"], "increase")
        return Response(status_code=status.HTTP_204_NO_CONTENT, description=f"User bet with id: {id} deleted")

    raise HTTPException(status_code=404, detail=f"User with id: {id} not found")


async def delete_comment(id: str):
    delete_result = await comments_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        message = f"Deleted comment: {id}"
        mqtt_client.publish("logs", message)
        return Response(status_code=status.HTTP_204_NO_CONTENT, description=f"Comment with id: {id} deleted")
