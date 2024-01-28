import json


def on_chat_message(client, userdata, message):
    message_data = json.loads(message.payload.decode("utf-8"))
    print(f"{message_data['username']}: {message_data['message']}")


def on_connect(client, userdata, flags, rc):
    # client.subscribe("bets/created")
    # client.subscribe("bets/resolved")
    client.subscribe("user/balanceChanged")
    client.message_callback_add("chat/all", on_chat_message)
    # client.subscribe("scoreboard/change")

