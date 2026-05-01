import socket

import socket
import json
from datetime import datetime

TCP_PORT    = 55001
BUFFER_SIZE = 4096

def tcp_server(username):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", TCP_PORT))
    sock.listen(5)

    while True:
        conn, addr = sock.accept()
        data = conn.recv(BUFFER_SIZE)
        msg  = json.loads(data.decode())

        if msg["type"] == "direct":
            print(f"\n[{msg['time']}] {msg['username']} → you: {msg['message']}")
            print("> ", end="", flush=True)

        conn.close()

def send_direct(username, target_ip, message):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target_ip, TCP_PORT))

        packet = json.dumps({
            "type":     "direct",
            "username": username,
            "message":  message,
            "time":     datetime.now().strftime("%H:%M")
        }).encode()

        sock.sendall(packet)
        sock.close()
        print(f"  ✓ message sent")

    except Exception:
        print(f"  ✗ could not reach that user")