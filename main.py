import os
import sys
import ctypes
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init
from pystyle import Write, Colors

init()
os.system("cls")

def set_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

def log(text):
    Write.Print(text, Colors.red_to_white, interval=0.00)

def send_webhook(url, content, username):
    try:
        payload = {
            "content": content,
            "username": username,
            "avatar_url": "https://raw.githubusercontent.com/duckboxxer/asset_rat_id_49e3fs303/refs/heads/main/depositphotos_63079503-stock-photo-clown.jpg"
        }
        response = requests.post(url, json=payload)

        if response.status_code in [200, 204]:
            print(f"{Fore.GREEN}[+] {Fore.RESET} Sent ({response.status_code})")
        elif response.status_code == 429:
            retry_after = response.json().get("retry_after", 1000) / 1000
            print(f"{Fore.RED}[!] {Fore.RESET}Rate limited ~ Retrying in {retry_after}s")
            time.sleep(retry_after)
            send_webhook(url, content, username)
        else:
            print(f"{Fore.RED}[-] {Fore.RESET}Failed with status {response.status_code}")
    except Exception as e:
        print(f"{Fore.RED}[-] {Fore.RESET}{e}")

def start_webhook_spam():
    url = Write.Input("~@RAT/WEBHOOK | ", Colors.red_to_white, interval=0.00)

    try:
        check = requests.get(url)
    except Exception as e:
        print(f"{Fore.RED}[ERROR] {Fore.RESET}Invalid URL: {e}")
        sys.exit()

    print(f"{Fore.YELLOW}[INFO] {Fore.RESET}Checking Webhook...")

    if check.status_code == 200:
        print(f"{Fore.GREEN}[INFO] {Fore.RESET}\n Webhook is valid!")
        message = Write.Input("~@RAT/MESSAGE | ", Colors.red_to_white, interval=0.00)
        username = Write.Input("~@RAT/USERNAME | ", Colors.red_to_white, interval=0.00)

        try:
            count = int(Write.Input("~@RAT/COUNT | ", Colors.red_to_white, interval=0.00))
        except ValueError:
            print(f"{Fore.RED}[-] {Fore.RESET}COUNT must be a number.")
            return

        with ThreadPoolExecutor(max_workers=4) as executor:
            for _ in range(count):
                executor.submit(send_webhook, url, message, username)
    else:
        print(f"{Fore.RED}[INFO] {Fore.RESET}Webhook is invalid")
        input("Press Enter To Exit")
        sys.exit()

ascii_logo = r"""
   ___  ___ ______
  / _ \/ _ /_  __/
 / , _/ __ |/ /   
/_/|_/_/ |_/_/    
"""

def main():
    set_title("Ratted Ratted Rat 🐀")
    log(ascii_logo)
    start_webhook_spam()

main()
