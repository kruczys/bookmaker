import asyncio

from bson import ObjectId

from server.cruds import user_bets_collection, update_user_balance, resolve_user_bet, \
    get_all_bets
from server.main import mqtt_client


class BetManager:
    def __init__(self, client):
        self.client = client

    async def resolve_bets(self):
        bets = await get_all_bets()
        for bet in bets:
            user_bets = await user_bets_collection.find({"bet_id": str(bet['_id']), "resolved": False}).to_list(length=1000)
            print(f"Bet '{bet['_id']}' has the following unresolved user bets: {user_bets}")
            for user_bet in user_bets:
                if bet['result'] == user_bet['option']:
                    try:
                        await update_user_balance(user_bet['user_id'], user_bet['amount'] * 1.67, "increase")
                    except Exception as e:
                        print(e)
                await resolve_user_bet(user_bet['_id'])
                self.client.publish("bets/resolved", f"{bet['title']} just got resolved")


async def main():
    client = mqtt_client
    bet_manager = BetManager(client)
    while True:
        await bet_manager.resolve_bets()
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
