import json
from typing import List

import paho.mqtt.client as mqtt
from fastapi import FastAPI
from fastapi import HTTPException
from starlette import status

from cruds import delete_comment, update_comment, get_comments_by_bet_id, create_comment, delete_user_bet, \
    get_user_bet_by_id, create_user_bet, delete_bet, update_bet, get_bet_by_id, create_bet, get_user_by_id, \
    update_user_balance, delete_user, create_user, get_all_users
from models import Comment, UserBet, Bet, User

app = FastAPI()

client = mqtt.Client()
client.connect("localhost", 1883)
client.loop_start()


def on_chat_message(client, userdata, message):
    message_data = json.loads(message.payload.decode("utf-8"))
    print(f"{message_data['username']}: {message_data['message']}")


def on_connect(client, userdata, flags, rc):
    # client.subscribe("bets/created")
    # client.subscribe("bets/resolved")
    # client.subscribe("comments/new")
    client.message_callback_add("chat/all", on_chat_message)
    # client.subscribe("scoreboard/change")


client.on_connect = on_connect


@app.get(
    "/auth/users",
    response_model_by_alias=False,
    response_model=List[User]
)
async def api_get_all_users():
    users = await get_all_users()
    return users


@app.post(
    "/auth/signup",
    response_model=User,
    response_description="Create user",
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def api_create_user(user: User):
    response = await create_user(user)
    return response


@app.delete("/auth/delete/{user_id}")
async def api_delete_user(user_id: str):
    response = await delete_user(user_id)
    return response


@app.put(
    "/auth/update_balance/{user_id}/{amount}/{operation}",
    response_model=User,
    response_model_by_alias=False,
)
async def api_update_user_balance(user_id: str, amount: float, operation: str):
    response = await update_user_balance(user_id, amount, operation)
    return response


@app.get(
    "/auth/user/{id}",
    response_description="User details",
    response_model=User,
    response_model_by_alias=False,
)
async def api_get_user(id: str):
    response = await get_user_by_id(id)
    return response


@app.post(
    "/bet",
    response_model=Bet,
    response_description=False,
)
async def api_create_bet(bet: Bet):
    response = await create_bet(bet)
    client.publish("bets/created", json.dumps({"message": f"New bet added: {bet.title}!"}))
    return response


@app.get("/bet/{bet_id}")
async def api_get_bet(bet_id: str):
    bet = await get_bet_by_id(bet_id)
    if bet:
        return bet
    raise HTTPException(status_code=404, detail="Bet not found")


@app.put("/bet/{bet_id}")
async def api_update_bet(bet_id: str, update_data: dict):
    await update_bet(bet_id, update_data)
    return {"message": "Bet updated successfully"}


@app.delete("/bet/{bet_id}")
async def api_delete_bet(bet_id: str):
    await delete_bet(bet_id)
    return {"message": "Bet deleted successfully"}


@app.post("/user_bets")
async def api_create_user_bet(user_bet: UserBet):
    await create_user_bet(user_bet)
    return {"message": "User's bet created successfully"}


@app.get("/user_bets/{user_bet_id}")
async def api_get_user_bet(user_bet_id: str):
    user_bet = await get_user_bet_by_id(user_bet_id)
    if user_bet:
        return user_bet
    raise HTTPException(status_code=404, detail="User's bet not found")


@app.delete("/user_bets/{user_bet_id}")
async def api_delete_user_bet(user_bet_id: str):
    await delete_user_bet(user_bet_id)
    return {"message": "User's bet deleted successfully"}


@app.post("/comment/{bet_id}")
async def api_create_comment(comment: Comment):
    await create_comment(comment)
    return {"message": "Comment created successfully"}


@app.get("/comment/{bet_id}")
async def api_get_comments(bet_id: str):
    comments = await get_comments_by_bet_id(bet_id)
    if comments:
        return {"comments": comments}
    raise HTTPException(status_code=404, detail="Comments not found")


@app.put("/comments/{comment_id}")
async def api_update_comment(comment_id: str, new_text: str):
    await update_comment(comment_id, new_text)
    return {"message": "Comment updated successfully"}


@app.delete("/comments/{comment_id}")
async def api_delete_comment(comment_id: str):
    await delete_comment(comment_id)
    return {"message": "Comment deleted successfully"}
