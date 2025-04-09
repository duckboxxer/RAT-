import requests
import pystyle
import concurrent
import os
import ctypes
import colorama
import time
from colorama import *
from pystyle import *
from concurrent.futures import ThreadPoolExecutor

os.system("cls")

def log(text):
    Write.Print(text, Colors.red_to_white, interval=0.00)

def title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

def webhook_nekoboy(url, content, username):
    try:
        payload = {
            "content": content,
            "username": username
        }
        r = requests.post(url, json=payload)
        if r.status_code == 204 or r.status_code == 200:
            print(f"{Fore.GREEN}[+] {Fore.RESET} {r.status_code}")
        elif r.status_code == 429:
            retry_after = r.json().get("retry_after", 1000) / 1000 
            print(f"{Fore.RED}[!] {Fore.RESET} RATELIITED ~ Retrying in {retry_after}s ")
    except Exception as e:
        print(f"{Fore.RED}[-] {Fore.RESET}{e}")

def webhook_fuckoff():
    URL = Write.Input("~@RAT/WEBHOOK | ", Colors.red_to_black, interval=0.00)
    check = requests.get(URL)

    print(f"{Fore.YELLOW}[INFO] {Fore.RESET}\n Checking Webhook")

    if check.status_code == 200:
        print(f"{Fore.GREEN}[INFO] {Fore.RESET}\n Webhook is valid!")
        messages = Write.Input("~@RAT/MESSAGE | ", Colors.red_to_black, interval=0.00)
        Username = Write.Input("~@RAT/USERNAME | ", Colors.red_to_black, interval=0.00)
        amount = int(Write.Input("~@RAT/COUNT | ", Colors.red_to_black, interval=0.00))

        with ThreadPoolExecutor(max_workers=5) as executor:
            for _ in range(amount):
                executor.submit(webhook_nekoboy, URL, messages, Username)
                executor.submit(webhook_nekoboy, URL, messages, Username)
                executor.submit(webhook_nekoboy, URL, messages, Username)
    else:
        print(f"{Fore.RED}[INFO] {Fore.RESET}\n Webhook is invalid")
        input("Press Enter To Exit")
        time.sleep(0.3)
        os.system("exit")

asciilogo = f"""
   ___  ___ ______
  / _ \/ _ /_  __/
 / , _/ __ |/ /   
/_/|_/_/ |_/_/    

"""

def main():
    log(asciilogo)
    webhook_fuckoff()

main()
