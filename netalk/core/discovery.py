import json
import socket
import time
import threading

BROADCAST_PORT     = 55000
BROADCAST_INTERVAL = 3
PEERS_EXPIRE       = 10
BUFFER_SIZE        = 4096

peers      = {}
peers_lock = threading.Lock()


def get_local_ips():
    ips = set()
    ips.add("127.0.0.1")
    try:
        hostname = socket.gethostname()
        results  = socket.getaddrinfo(hostname, None)
        for result in results:
            ips.add(result[4][0])
    except Exception:
        pass
    return ips


def broadcast_presence(username, ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    beacon = json.dumps({
        "type":     "hello",
        "username": username,
        "ip":       ip
    }).encode()

    while True:
        s.sendto(beacon, ("255.255.255.255", BROADCAST_PORT))
        time.sleep(BROADCAST_INTERVAL)


def listen_for_peers(ip):
    local_ips = get_local_ips()
    local_ips.add(ip)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", BROADCAST_PORT))

    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        sender_ip = addr[0]

        if sender_ip in local_ips:
            continue

        message = json.loads(data.decode())

        if message["type"] == "hello":
            with peers_lock:
                peers[sender_ip] = {
                    "username":  message["username"],
                    "last_seen": time.time()
                }
        elif message["type"] == "global":
            print(f"\n[{message['time']}] {message['username']}: {message['message']}")
            print("> ", end="", flush=True)

        elif message["type"] == "goodbye":
            with peers_lock:
                if sender_ip in peers:
                    del peers[sender_ip]
            print(f"\n  {message['username']} left the network")
            print("> ", end="", flush=True)


def expire_peers():
    while True:
        now = time.time()
        with peers_lock:
            expired = [ip for ip, info in peers.items() if now - info["last_seen"] > PEERS_EXPIRE]
            for ip in expired:
                del peers[ip]
        time.sleep(2)


def send_goodbye(username, ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    packet = json.dumps({
        "type":     "goodbye",
        "username": username,
        "ip":       ip
    }).encode()

    s.sendto(packet, ("255.255.255.255", BROADCAST_PORT))
    s.close()