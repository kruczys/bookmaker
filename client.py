from datetime import datetime
from random import randint

import requests

BASE_URL = 'http://127.0.0.1:8000/'
client_user = {"username": ""}


def create_user():
    username = input('Enter your username: ')
    balance = 1000
    data = {
        "username": username,
        "balance": balance
    }
    response = requests.post(url=BASE_URL + 'auth/signup', json=data)
    if response.status_code == 200:
        print(response.json().get('message'))
        client_user['username'] = username
    else:
        print("Something went wrong...")


def create_bet():
    creator_username = client_user['username']
    bet_text = input('Enter your bet text: ')
    bet_year = input('Enter your bet resolve year: ')
    bet_month = input('Enter your bet resolve month: ')
    bet_day = input('Enter your bet resolve day: ')
    bet_hour = input('Enter your bet resolve hour: ')
    bet_minute = input('Enter your bet resolve minute: ')
    resolve_date = datetime(year=int(bet_year),
                            month=int(bet_month),
                            day=int(bet_day),
                            hour=int(bet_hour),
                            minute=int(bet_minute))
    data = {
        "creator_username": creator_username,
        "title": bet_text,
        "resolve_date": resolve_date.isoformat(),
    }

    response = requests.post(url=BASE_URL + 'bet', json=data)
    if response.status_code == 200:
        return response.json().get('message')
    else:
        "Something went wrong..."


def get_bets():
    response = requests.get(url=BASE_URL + 'bet')
    if response.status_code == 200:
        return response.json().get('bets')
    else:
        return "Something went wrong..."


create_user()
create_bet()
print(get_bets())
