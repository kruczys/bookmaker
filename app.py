import requests

BASE_URL = 'http://localhost:8000/'


def fetch_bets():
    response = requests.get(f'{BASE_URL}bets/')
    if response.status_code == 200:
        bets = response.json()
        for bet in bets:
            print(f"Bet ID: {bet['id']}")
            print(f"Bet Text: {bet['bet_text']}")
            print(f"Resolve Date: {bet['resolve_date']}")
            print(f"Result: {bet['result']}")
            print(f"Resolved: {bet['resolved']}")
            print("-------------------------------")
    else:
        print("Error while fetching bets. HTTP Status Code: ", response.status_code)


def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(f'{BASE_URL}/login', data=data)
    if response.text:  # Make sure response is not empty
        try:
            json_response = response.json()
            print(json_response["message"])
        except ValueError:  # Includes simplejson.errors.JSONDecodeError
            print("Decoding JSON has failed")
    elif response.status_code == 200:
        print("Login successful, but no message received.")
    else:
        print("No response from the server.")


fetch_bets()
login()
