import asyncio

import paho.mqtt.client as mqtt

from server.cruds import user_bets_collection, update_user_balance, resolve_user_bet, \
    get_all_bets

mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883)


class BetManager:
    def __init__(self, client):
        self.client = client

    async def resolve_bets(self):
        bets = await get_all_bets()
        for bet in bets:
            user_bets = await user_bets_collection.find({"bet_id": str(bet['_id']), "resolved": False}).to_list(
                length=1000)
            print(f"Bet '{bet['_id']}' has the following unresolved user bets: {user_bets}")
            for user_bet in user_bets:
                if bet['result'] == user_bet['option']:
                    try:
                        await update_user_balance(user_bet['user_id'], user_bet['amount'] * 1.67, "increase")
                    except Exception as e:
                        print(e)
                await resolve_user_bet(user_bet['_id'])


async def main():
    client = mqtt_client
    bet_manager = BetManager(client)
    client.publish("bet_manager/working", "Started work")
    while True:
        client.publish("bet_manager/working", "Resolving bets")
        await bet_manager.resolve_bets()
        await asyncio.sleep(30)


if __name__ == "__main__":
    asyncio.run(main())
