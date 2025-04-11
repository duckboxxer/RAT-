import os
import sys
import ctypes
import time
import requests
import random
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init
import base64
from pystyle import Write, Colors

init()
os.system("cls")

def set_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

def log(text):
    Write.Print(text, Colors.red_to_white, interval=0.00)

def proxy_config():
    proxy_file = "proxies.txt"
    if not os.path.exists(proxy_file):
        print(f"{Fore.YELLOW}[INFO] {Fore.RESET} proxies.txt not found!")
        return None

    try:
        with open(proxy_file, "r") as file:
            proxies = [line.strip() for line in file if line.strip()]
            if not proxies:
                print(f"{Fore.YELLOW}[INFO] {Fore.RESET} No Proxies Mode")
                return None

            randomproxies = random.choice(proxies)
            ip, port, user, password = randomproxies.split(":")
            proxy_auth = f"{user}:{password}@{ip}:{port}"
            proxy_url = f"http://{proxy_auth}"

            return {
                "http": proxy_url,
                "https": proxy_url
            }

    except Exception as e:
        print(f"{Fore.RED}[-] {Fore.RESET}proxies.txt Error: {e}")
        return None

def send_webhook(url, content, username, proxies):
    try:
        payload = {
            "content": content,
            "username": username,
            "avatar_url": "https://raw.githubusercontent.com/duckboxxer/asset_rat_id_49e3fs303/refs/heads/main/depositphotos_63079503-stock-photo-clown.jpg"
        }
        response = requests.post(url, json=payload, proxies=proxies)

        if response.status_code in [200, 204]:
            print(f"{Fore.GREEN}[+] {Fore.RESET} Sent ({response.status_code})")
        elif response.status_code == 429:
            retry_after = response.json().get("retry_after", 1000) / 1000
            print(f"{Fore.RED}[!] {Fore.RESET}Rate limited ~ Retrying in {retry_after}s")
            time.sleep(retry_after)
            send_webhook(url, content, username, proxies)
        else:
            print(f"{Fore.RED}[-] {Fore.RESET} Failed with status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[-] {Fore.RESET}Request error: {e}")
    except Exception as e:
        print(f"{Fore.RED}[-] {Fore.RESET}Unexpected error: {e}")

def start_webhook_spam():
    url = Write.Input("~@RAT/WEBHOOK | ", Colors.red_to_white, interval=0.00)

    try:
        check = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[ERROR] {Fore.RESET}Invalid URL: {e}")
        sys.exit()

    print(f"{Fore.YELLOW}[INFO] {Fore.RESET}Checking Webhook...")

    if check.status_code == 200:
        print(f"{Fore.GREEN}[INFO] {Fore.RESET}\n \n Webhook is valid!")

        message = Write.Input("~@RAT/MESSAGE | ", Colors.red_to_white, interval=0.00)
        username = Write.Input("~@RAT/USERNAME | ", Colors.red_to_white, interval=0.00)

        try:
            count = int(Write.Input("~@RAT/COUNT | ", Colors.red_to_white, interval=0.00))
        except ValueError:
            print(f"{Fore.RED}[-] {Fore.RESET}COUNT must be a number.")
            return

        proxies = proxy_config()

        if proxies:
            max_threads = min(count, 10)  
            with ThreadPoolExecutor(max_workers=max_threads) as executor:
                for _ in range(count):
                    executor.submit(send_webhook, url, message, username, proxies)
        else:
            print(f"{Fore.RED}[-] {Fore.RESET}Failed to load proxy settings")

    else:
        print(f"{Fore.RED}[INFO] {Fore.RESET}\n \nWebhook is invalid")
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
