import json
from typing import List

import paho.mqtt.client as mqtt
from fastapi import FastAPI
from starlette import status

from server.cruds import delete_comment, get_comments_by_bet_id, create_comment, delete_user_bet, \
    get_user_bet_by_id, create_user_bet, delete_bet, get_bet_by_id, create_bet, get_user_by_id, \
    update_user_balance, delete_user, create_user, get_all_users, update_comment_text, update_bet_title, \
    get_all_user_bets, get_unresolved_bets, get_resolved_bets
from server.models import Comment, UserBet, Bet, User
from server.mqtt import on_connect

app = FastAPI()

mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883)
mqtt_client.loop_start()
mqtt_client.on_connect = on_connect


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
    "/bets",
    response_model=Bet,
    response_description=False,
)
async def api_create_bet(bet: Bet):
    response = await create_bet(bet)
    mqtt_client.publish("bets/created", json.dumps({"message": f"New bet added: {bet.title}!"}))
    return response


@app.get(
    "/bets/unresolved",
    response_model=List[Bet],
    response_model_by_alias=False,
)
async def api_get_unresolved_bets():
    response = await get_unresolved_bets()
    return response


@app.get(
    "/bets/resolved",
    response_model=List[Bet],
    response_model_by_alias=False,
)
async def api_get_resolved_bets():
    response = await get_resolved_bets()
    return response


@app.get(
    "/bets/{bet_id}",
    response_model=Bet,
    response_model_by_alias=False,
)
async def api_get_bet(bet_id: str):
    response = await get_bet_by_id(bet_id)
    return response


@app.put(
    "/bets/{bet_id}",
    response_model=Bet,
    response_model_by_alias=False,
)
async def api_update_bet(bet_id: str, new_title: str):
    response = await update_bet_title(bet_id, new_title)
    return response


@app.delete("/bets/{bet_id}")
async def api_delete_bet(bet_id: str):
    response = await delete_bet(bet_id)
    return response


@app.get(
    "/user_bets",
    response_model=List[UserBet],
    response_model_by_alias=False,
)
async def api_get_all_user_bets(user_id: str):
    response = await get_all_user_bets(user_id)
    return response


@app.post(
    "/user_bets",
    response_model=UserBet,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED,
)
async def api_create_user_bet(user_bet: UserBet):
    response = await create_user_bet(user_bet)
    return response


@app.get(
    "/user_bets/{user_bet_id}",
    response_model=UserBet,
    response_model_by_alias=False,
)
async def api_get_user_bet(user_bet_id: str):
    response = await get_user_bet_by_id(user_bet_id)
    return response


@app.delete("/user_bets/{user_bet_id}")
async def api_delete_user_bet(user_bet_id: str):
    response = await delete_user_bet(user_bet_id)
    return response


@app.post(
    "/comments/{bet_id}",
    response_model=Comment,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED,
)
async def api_create_comment(comment: Comment):
    response = await create_comment(comment)
    return response


@app.get(
    "/comments/{bet_id}",
    response_model=List[Comment],
    response_model_by_alias=False,
)
async def api_get_comments(bet_id: str):
    response = await get_comments_by_bet_id(bet_id)
    return response


@app.put(
    "/comments/{comment_id}",
    response_model=Comment,
    response_model_by_alias=False,
)
async def api_update_comment_text(comment_id: str, new_text: str):
    response = await update_comment_text(comment_id, new_text)
    return response


@app.delete("/comments/{comment_id}")
async def api_delete_comment(comment_id: str):
    response = await delete_comment(comment_id)
    return response
