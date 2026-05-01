def show_welcome(username, is_new):
    if is_new:
        print(f"Welcome, {username}!")
    else:
        print(f"Welcome back, {username}!")
    print("To find out how to use the tool write help")
    print()

def show_help():
    print("""
  help                        — show this message
  /discover                   — scan for people on the network
  /list                       — show discovered peers
  /global <message>           — send a message to everyone
  /send -u <username> <message> — send a direct message
  /quit                       — exit
    """)

def show_peers(peers):
    if not peers:
        print("  No peers found yet. Try /discover first.")
        return
    print(f"\n  {'USERNAME':<20} {'IP'}")
    print("  " + "─" * 35)
    for ip, info in peers.items():
        print(f"  {info['username']:<20} {ip}")
    print()

def show_error(message):
    print(f"  ✗ {message}")

def show_success(message):
    print(f"  ✓ {message}")