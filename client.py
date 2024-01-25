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

    def get_my_balance(self, username: str) -> str:
        response = requests.get(f"{self.base_url}/auth/user_balance/{username}")
        client_logs.append({f"GET_MY_BALANCE {datetime.now()}": response.json()})
        return response.json()["balance"]

    def create_bet(self, username: str, title: str, resolve_date: str):
        data = {"creator_username": username,
                "title": title,
                "resolve_date": resolve_date,
                "result": randint(0, 2)
                }
        response = requests.post(f"{self.base_url}/bet", json=data)
        client_logs.append({f"CREATE_BET {datetime.now()}": response.json()})
        return "BET CREATED"

    def get_bets(self):
        response = requests.get(f"{self.base_url}/bet")
        client_logs.append({f"GET_BETS {datetime.now()}": response.json()})
        return response.json()

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

    def create_user_bet(self, user_id: str, bet_title: str, amount: float, option: int) -> None:
        bet_id = self.get_bet_id(bet_title)
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
    cli.signup_user(username)

    while True:
        cli.clear_console()
        print("KOMENDY")
        print("ENTER_CHAT, EXIT_CHAT"),
        print("LEAVE_BYE, CLEAR_CONSOLE"),
        print("CHANGE_USERNAME, SHOW_BALANCE, SHOW_MY_BETS, SHOW_SCOREBOARD, DELETE_ME, SHOW_MY_ID")
        print("SHOW_COMMENT, CREATE_COMMENT, DELETE_COMMENT, UPDATE_COMMENT, SEARCH_USER_COMMENT")
        print("SHOW_BETS, BET_SOMETHING, DELETE_WAGERED_BET, CREATE_BET, DELETE_CREATED_BET, UPDATE_CREATED_BET_TITLE")
        user_command = input("Twoja komenda: ")

        match user_command:
            case "ENTER_CHAT":
                cli.clear_console()
                while user_command != "EXIT_CHAT":
                    user_command = input()
                    client.subscribe("chat/all")
                    cli.chat(username, user_command)
            case "EXIT_CHAT":
                print("You left the chat.")
                time.sleep(2)
                client.unsubscribe("chat/all")
            case "CHANGE_USERNAME":
                new_username = input("Enter your new username: ")
                cli.update_username(username, new_username)
                username = new_username
            case "LEAVE_BYE":
                print("Goodbye!")
                break
            case "CLEAR_CONSOLE":
                cli.clear_console()
            case "SHOW_BALANCE":
                print(cli.get_my_balance(username))
                input()
            case "SHOW_MY_BETS":
                user_id = cli.get_my_id(username)
                cli.get_user_bets(user_id)
            case "SHOW_SCOREBOARD":
                cli.get_bets()
            case "DELETE_ME":
                cli.delete_user(username)
                print("User deleted. Exiting the application.")
                break
            case "SHOW_MY_ID":
                user_id = cli.get_my_id(username)
                print(f"Your user ID is: {user_id}")
            case "SHOW_COMMENT":
                bet_id = input("Enter the bet ID to show comments for: ")
                cli.get_comments_by_bet_id(bet_id)
            case "CREATE_COMMENT":
                bet_id = input("Enter the bet ID to comment on: ")
                text = input("Enter your comment: ")
                cli.create_comment(bet_id, username, text)
            case "DELETE_COMMENT":
                bet_id = input("Enter the bet ID for the comment to delete: ")
                cli.delete_comment(bet_id, username)
            case "UPDATE_COMMENT":
                bet_id = input("Enter the bet ID for the comment to update: ")
                new_text = input("Enter your new comment: ")
                cli.update_user_comment(bet_id, username, new_text)
            case "SEARCH_USER_COMMENT":
                username_substring = input("Enter the username substring to search for in comments: ")
                cli.search_user_comment(username_substring)
            case "SHOW_BETS":
                bets = cli.get_bets()["bets"]
                for bet in bets:
                    print(bet["title"], f"{bet["resolve_date"]}")
                input()
            case "BET_SOMETHING":
                bet_title = input("Enter the bet title you want to bet on: ")
                amount = float(input("Enter the amount you want to bet: "))
                option = int(input("Enter your option (0, 1, or 2): "))
                user_id = cli.get_my_id(username)
                cli.create_user_bet(user_id, bet_title, amount, option)
            case "DELETE_WAGERED_BET":
                bet_id = input("Enter the bet ID of the bet you want to delete: ")
                user_id = cli.get_my_id(username)
                cli.delete_user_bet(bet_id, user_id)
            case "CREATE_BET":
                title = input("Enter the title of the bet: ")
                resolve_year = int(input("Enter the resolve year: "))
                resolve_month = int(input("Enter the resolve month: "))
                resolve_day = int(input("Enter the resolve day: "))
                resolve_hour = int(input("Enter the resolve hour: "))
                resolve_minute = int(input("Enter the resolve minute: "))
                resolve_date = datetime(
                    year=resolve_year,
                    month=resolve_month,
                    day=resolve_day,
                    hour=resolve_hour,
                    minute=resolve_minute)
                cli.create_bet(username, title, resolve_date.isoformat())
            case "DELETE_CREATED_BET":
                title = input("Enter the title of the bet you want to delete: ")
                cli.delete_bet(title, username)
            case "UPDATE_CREATED_BET_TITLE":
                old_title = input("Enter the current title of the bet: ")
                new_title = input("Enter the new title of the bet: ")
                cli.update_bet_title(old_title, new_title, username)
            case _:
                print("Unknown command. Please try again.")


if __name__ == "__main__":
    main()
