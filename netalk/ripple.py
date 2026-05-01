import os
import threading
import socket
import json

from core.discovery import broadcast_presence, listen_for_peers, expire_peers
from core.messaging import tcp_server
from cli.commands import start_cli

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

ip = get_local_ip()
os.makedirs("data", exist_ok=True)

if os.path.exists("data/user.json"):
    with open("data/user.json", "r") as f:
        data = json.load(f)
        username = data["username"]
        print(f"Welcome back, {username}!")
        print("Write help to find out how to use my tool!")
else:
    username = input("Enter your username: ")
    with open("data/user.json", "w") as f:
        json.dump({"username": username, "ip": ip}, f)
    print(f"Welcome, {username}!")
    print("Write help to find out how to use my tool!")

threading.Thread(target=broadcast_presence, args=(username, ip), daemon=True).start()
threading.Thread(target=listen_for_peers, args=(ip,), daemon=True).start()
threading.Thread(target=tcp_server, args=(username,), daemon=True).start()
threading.Thread(target=expire_peers, daemon=True).start()

start_cli(username, ip)
