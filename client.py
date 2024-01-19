from datetime import datetime
from random import randint

import requests

BASE_URL = 'http://127.0.0.1:8000'
client_user = {"username": ""}
client_logs = []


class CommandLineInterface:
    def __init__(self, base_url):
        self.base_url = base_url

    def signup_user(self, username):
        data = {"username": username, "balance": 1000}
        response = requests.post(f"{self.base_url}/auth/signup", json=data)
        client_logs.append({f"SIGNUP_USER {datetime.now()}": response.json()})

    def delete_user(self, username):
        response = requests.delete(f"{self.base_url}/auth/delete/{username}")
        client_logs.append({f"DELETE_USER {datetime.now()}": response.json()})

    def update_username(self, old_username, new_username):
        response = requests.put(f"{self.base_url}/auth/update_username/{old_username}/{new_username}")
        client_logs.append({f"UPDATE_USERNAME {datetime.now()}": response.json()})

    def get_my_id(self, username):
        response = requests.get(f"{self.base_url}/auth/user_id/{username}")
        client_logs.append({f"GET_MY_ID {datetime.now()}": response.json()})

    def get_my_balance(self, username):
        response = requests.get(f"{self.base_url}/auth/user_balance/{username}")
        client_logs.append({f"GET_MY_BALANCE {datetime.now()}": response.json()})

    def create_bets(self, username, title, resolve_date):
        data = {"creator_username": username,
                "title": title,
                "resolve_date": resolve_date,
                "result": randint(0, 2)
                }
        response = requests.post(f"{self.base_url}/bet", json=data)
        client_logs.append({f"CREATE_BET {datetime.now()}": response.json()})

    def get_bets(self):
        response = requests.get(f"{self.base_url}/bet")
        client_logs.append({f"GET_BETS {datetime.now()}": response.json()})

    def search_bets(self, title_substring):
        response = requests.get(f"{self.base_url}/bet/search?q={title_substring}")
        client_logs.append({f"SEARCH_BET {datetime.now()}": response.json()})


def main():
    cli = CommandLineInterface(BASE_URL)
    username = input("Enter your username: ")
    cli.signup_user(username)
    cli.get_my_id(username)
    cli.get_my_balance(username)
    cli.update_username(username, username + "@example.com")
    cli.create_bets(username, title="My bet", resolve_date=datetime.now().isoformat())
    cli.get_bets()
    cli.search_bets("be")
    cli.delete_user(username + "@example.com")
    for log in client_logs:
        print(log, "\n")


if __name__ == "__main__":
    main()
