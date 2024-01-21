import json
import os
import time
from datetime import datetime
from random import randint

import requests

from main import client

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

    def update_user_comment(self, bet_id: str, creator_username: str, new_text: str = "") -> None:
        response = requests.put(f"{self.base_url}/{bet_id}/{creator_username}?new_text={new_text}")
        client_logs.append({f"UPDATE_USER_COMMENT {datetime.now()}": response.json()})

    def delete_comment(self, bet_id: str, creator_username: str) -> None:
        response = requests.delete(f"{self.base_url}/{bet_id}/{creator_username}")
        client_logs.append({f"DELETE_COMMENT {datetime.now()}": response.json()})

    def chat(self, username: str, message: str):
        data = {"username": username, "message": message}
        client.publish("chat/all", json.dumps(data))

    def clear_console(self) -> None:
        if os.name == "nt":
            os.system('cls')
        else:
            os.system("clear")


def main():
    cli = CommandLineInterface(BASE_URL)
    username = input("wpisz swoj nick: ")

    while True:
        cli.clear_console()
        print("Spis komend: ENTER_CHAT, EXIT_CHAT, CHANGE_USERNAME, LEAVE_BYE, CLEAR_CONSOLE, SHOW_BETS, SHOW_BALANCE")
        user_command = input("Twoja komenda: ")

        match user_command:
            case "ENTER_CHAT":
                cli.clear_console()
                while user_command != "EXIT_CHAT":
                    user_command = input()
                    client.subscribe("chat/all")
                    cli.chat(username, user_command)
            case "EXIT_CHAT":
                print("WYSZEDLES Z CHATU")
                time.sleep(2)
                client.unsubscribe("chat/all")
            case "LEAVE_BYE":
                print("BYE BYE")
                break


if __name__ == "__main__":
    main()
