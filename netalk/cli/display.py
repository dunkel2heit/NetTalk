def show_welcome(username, is_new):
    if is_new:
        print(f"Welcome, {username}!")
    else:
        print(f"Welcome back, {username}!")
    print("Write help to find out how to use my tool!")
    print()

def show_help():
    print("""
  help                          — show this message
  /discover                     — scan for people on the network
  /list                         — show discovered peers
  /global <message>             — send a message to everyone
  /send -u <username> <message> — send a direct message
  /quit                         — exit
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

def show_error(msg):
    print(f"  ✗ {msg}")

def show_success(msg):
    print(f"  ✓ {msg}")