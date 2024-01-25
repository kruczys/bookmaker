from datetime import datetime, timedelta
from uuid import uuid4


def create_initial_game(User, Bet, UserBet, Comment, users, bets, user_bets):
    john = User(username='John', balance=1000.00)
    mary = User(username='Mary', balance=2000.00)
    adam = User(username='Adam', balance=1500.00)

    john_id = str(uuid4())
    mary_id = str(uuid4())
    adam_id = str(uuid4())

    bet1 = Bet(creator_username='John', title='Polska vs Japonia', resolve_date=datetime.now() + timedelta(minutes=1), result=0)
    bet2 = Bet(creator_username='Adam', title='Polska vs Wlochy', resolve_date=datetime.now() + timedelta(minutes=2), result=1)
    bet3 = Bet(creator_username='Mary', title='Wlochy vs Japonia', resolve_date=datetime.now() + timedelta(minutes=3), result=0)

    bet1_id = str(uuid4())
    bet2_id = str(uuid4())
    bet3_id = str(uuid4())

    userbet1 = UserBet(user_id=john_id, bet_id=bet1_id, amount=200.00, option=0)
    userbet2 = UserBet(user_id=mary_id, bet_id=bet2_id, amount=100.00, option=1)
    userbet3 = UserBet(user_id=adam_id, bet_id=bet3_id, amount=50.00, option=0)

    comment1 = Comment(bet_id=bet1_id, creator_username='John', text='Go for it!',
                       create_date=datetime.now())
    comment2 = Comment(bet_id=bet1_id, creator_username='Mary', text='Good Luck!',
                       create_date=datetime.now())
    comment3 = Comment(bet_id=bet1_id, creator_username='Adam', text='Wish me Luck!',
                       create_date=datetime.now())

    comments_local = [comment1, comment2, comment3]
    user_bets_local = [userbet1, userbet2, userbet3]
    bets_local = [bet1, bet2, bet3]
    users_local = [john, mary, adam]
    user_ids = [john_id, mary_id, adam_id]
    bet_ids = [bet1_id, bet2_id, bet3_id]

    for i in range(3):
        users[user_ids[i]] = users_local[i]
        bets[bet_ids[i]] = bets_local[i]
        user_bets.append(user_bets_local[i])
        comments_local.append(comments_local[i])


if __name__ == "__main__":
    create_initial_game()
