from cruds import user_bets_collection, get_resolved_bets, update_user_balance, resolve_user_bet


class BetManager:
    def __init__(self, client):
        self.client = client

    async def resolve_bets(self):
        resolved_bets = await get_resolved_bets()
        for bet in resolved_bets:
            user_bets = await user_bets_collection.find({"bet_id": bet['id'], "resolved": False})
            bet_dict = bet.model_dump(by_alias=True, exclude=["id"])
            user_bet_dict = user_bets.model_dump(by_alias=True, exclude=["id"])
            for user_bet in user_bets:
                if bet_dict['result'] == user_bet_dict['option']:
                    await update_user_balance(user_bet_dict['user_id'], user_bet_dict['amount'] * 1.67, "increase")
                await resolve_user_bet(user_bet_dict['id'])
                self.client.publish("bets/resolved", f"{bet_dict['title']} just got resolved")