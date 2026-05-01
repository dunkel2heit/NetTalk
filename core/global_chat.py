import socket
import json
from datetime import datetime

BROADCAST_PORT = 55000

def send_global(username, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    packet = json.dumps({
        "type":     "global",
        "username": username,
        "message":  message,
        "time":     datetime.now().strftime("%H:%M")
    }).encode()

    sock.sendto(packet, ("255.255.255.255", BROADCAST_PORT))
    sock.close()