import time
import threading
from core.discovery import peers, peers_lock
from core.global_chat import send_global
from core.messaging import send_direct
from cli.display import show_help, show_peers, show_error, show_success

def start_cli(username, ip):
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Goodbye!")
            break

        if not raw:
            continue

        # ── help ──────────────────────────────────────────
        elif raw == "help":
            show_help()

        # ── /list ─────────────────────────────────────────
        elif raw == "/list":
            with peers_lock:
                show_peers(peers)

        # ── /discover ─────────────────────────────────────
        elif raw == "/discover":
            print("  Scanning...")
            time.sleep(3)
            with peers_lock:
                show_peers(peers)

        # ── /global ───────────────────────────────────────
        elif raw.startswith("/global "):
            message = raw[8:]
            if message:
                send_global(username, message)
            else:
                show_error("Usage: /global <message>")

        # ── /send ─────────────────────────────────────────
        elif raw.startswith("/send -u "):
            parts = raw.split(" ", 3)
            if len(parts) < 4:
                show_error("Usage: /send -u <username> <message>")
                continue

            target_username = parts[2]
            message         = parts[3]

            target_ip = None
            with peers_lock:
                for peer_ip, info in peers.items():
                    if info["username"] == target_username:
                        target_ip = peer_ip
                        break

            if target_ip is None:
                show_error(f"User '{target_username}' not found. Try /discover first.")
            else:
                send_direct(username, target_ip, message)

        # ── /quit ─────────────────────────────────────────
        elif raw == "/quit":
            from core.discovery import send_goodbye
            send_goodbye(username, ip)
            print("  Goodbye!")
            break

        else:
            show_error("Unknown command. Type help to see available commands.")