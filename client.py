from datetime import datetime
from random import randint

import requests

BASE_URL = 'http://127.0.0.1:8000'
client_user = {"username": ""}
client_logs = []


class CommandLineInterface:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    def signup_user(self, username: str) -> None:
        data = {"username": username, "balance": 1000}
        response = requests.post(f"{self.base_url}/auth/signup", json=data)
        client_logs.append({f"SIGNUP_USER {datetime.now()}": response.json()})

    def delete_user(self, username: str) -> None:
        response = requests.delete(f"{self.base_url}/auth/delete/{username}")
        client_logs.append({f"DELETE_USER {datetime.now()}": response.json()})

    def update_username(self, old_username: str, new_username: str) -> None:
        response = requests.put(f"{self.base_url}/auth/update_username/{old_username}/{new_username}")
        client_logs.append({f"UPDATE_USERNAME {datetime.now()}": response.json()})

    def get_my_id(self, username: str) -> str:
        response = requests.get(f"{self.base_url}/auth/user_id/{username}")
        user_id = response.json()["user_id"]
        client_logs.append({f"GET_MY_ID {datetime.now()}": response.json()})
        return user_id

    def get_my_balance(self, username: str) -> None:
        response = requests.get(f"{self.base_url}/auth/user_balance/{username}")
        client_logs.append({f"GET_MY_BALANCE {datetime.now()}": response.json()})

    def create_bet(self, username: str, title: str, resolve_date: str) -> None:
        data = {"creator_username": username,
                "title": title,
                "resolve_date": resolve_date,
                "result": randint(0, 2)
                }
        response = requests.post(f"{self.base_url}/bet", json=data)
        client_logs.append({f"CREATE_BET {datetime.now()}": response.json()})

    def get_bets(self) -> None:
        response = requests.get(f"{self.base_url}/bet")
        client_logs.append({f"GET_BETS {datetime.now()}": response.json()})

    def search_bets(self, title_substring: str) -> None:
        response = requests.get(f"{self.base_url}/bet/search?q={title_substring}")
        client_logs.append({f"SEARCH_BET {datetime.now()}": response.json()})

    def get_bet_id(self, bet_title: str) -> str:
        response = requests.get(f"{self.base_url}/bet/bet_id/{bet_title}")
        bet_id = response.json()["bet_id"]
        client_logs.append({f"BET_ID {datetime.now()}": response.json()})
        return bet_id

    def update_bet_title(self, old_title: str, new_title: str, username: str) -> None:
        response = requests.put(f"{self.base_url}/bet/{old_title}/{username}/{new_title}")
        client_logs.append({f"UPDATE_BET_TITLE {datetime.now()}": response.json()})

    def delete_bet(self, title: str, username: str) -> None:
        response = requests.delete(f"{self.base_url}/bet/{title}/{username}")
        client_logs.append({f"DELETE_BET {datetime.now()}": response.json()})

    def create_user_bet(self, user_id: str, bet_id: str, amount: float, option: int) -> None:
        data = {
            "user_id": user_id,
            "bet_id": bet_id,
            "amount": amount,
            "option": option
        }
        response = requests.post(f"{self.base_url}/user_bets", json=data)
        client_logs.append({f"CREATE_USER_BET {datetime.now()}": response.json()})

    def get_user_bets(self, user_id: str) -> None:
        response = requests.get(f"{self.base_url}/user_bets/{user_id}")
        client_logs.append({f"GET_USER_BETS {datetime.now()}": response.json()})

    def delete_user_bet(self, bet_id: str, user_id: str) -> None:
        response = requests.delete(f"{self.base_url}/user_bets/{bet_id}/{user_id}")
        client_logs.append({f"DELETE_USER_BET {datetime.now()}": response.json()})

    def create_comment(self, bet_id: str, creator_username: str, text: str) -> None:
        data = {
            "bet_id": bet_id,
            "creator_username": creator_username,
            "text": text,
            "create_date": datetime.now().isoformat(),
            "likes": 0
        }
        response = requests.post(f"{self.base_url}/comment/{bet_id}", json=data)
        client_logs.append({f"CREATE_COMMENT {datetime.now()}": response.json()})

    def get_comments_by_bet_id(self, bet_id: str) -> None:
        response = requests.get(f"{self.base_url}/comment/{bet_id}")
        client_logs.append({f"GET_COMMENTS_BY_BET_ID {datetime.now()}": response.json()})

    def search_user_comment(self, username_substring: str) -> None:
        response = requests.get(f"{self.base_url}/comment/search?username_substring={username_substring}")
        client_logs.append({f"SEARCH_USER_COMMENTS {datetime.now()}": response.json()})

    def update_user_comment(self, bet_id: str, creator_username: str, partial_text: str = "") -> None:
        pass

    def delete_comment(self, bet_id: str, creator_username: str, partial_text: str = "") -> None:
        pass

    def chat(self):
        pass


def main():
    cli = CommandLineInterface(BASE_URL)
    username = input("Enter your username: ")
    cli.signup_user(username)
    cli.get_my_id(username)
    cli.get_my_balance(username)
    cli.update_username(username, username + "@example.com")
    cli.create_bet(username, title="My bet", resolve_date=datetime(year=2077, month=12, day=10).isoformat())
    cli.get_bets()
    cli.search_bets("be")
    cli.get_bet_id("My bet")
    cli.update_bet_title("My bet", "New bet title", username)
    cli.create_user_bet(cli.get_my_id(username + "@example.com"), cli.get_bet_id("New bet title"), 10.0, 1)
    cli.get_my_balance(username + "@example.com")
    cli.get_user_bets(cli.get_my_id(username + "@example.com"))
    cli.delete_bet("New bet title", username)
    cli.delete_user(username + "@example.com")
    for log in client_logs:
        print(log)


if __name__ == "__main__":
    main()
