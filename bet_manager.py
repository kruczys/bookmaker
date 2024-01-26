from cruds import user_bets_collection, get_resolved_bets, update_user_balance, resolve_user_bet


class BetManager:
    def __init__(self, client):
        self.client = client

    async def resolve_bets(self):
        resolved_bets = await get_resolved_bets()
        for bet in resolved_bets:
            user_bets = await user_bets_collection.find({"bet_id": bet['id'], "resolved": False})
            for user_bet in user_bets:
                if bet['result'] == user_bet['option']:
                    await update_user_balance(user_bet['user_id'], user_bet['amount'] * 1.67, "increase")
                await resolve_user_bet(user_bet['id'])
                self.client.publish("bets/resolved", f"{bet['title']} just got resolved")