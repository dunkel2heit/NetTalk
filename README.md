# Ripple 🌐

A lightweight LAN chat tool built in pure Python.
No internet connection required. No servers. No installation.
Just run it and talk to anyone on the same network.

## Features

- Auto peer discovery over UDP
- Global messages to everyone on the LAN
- Direct messages by username
- Clean disconnect notification
- Remembers your username between sessions

## Requirements

- Python 3.6+
- No external libraries — standard library only

## Usage

```bash
python ripple.py
```

On first launch you will be asked to choose a username.
On returning launches it loads your username automatically.

## Commands

| Command | Description |
|---|---|
| `help` | Show available commands |
| `/discover` | Scan for people on the network |
| `/list` | Show currently known peers |
| `/global <message>` | Send a message to everyone |
| `/send -u <username> <message>` | Send a direct message |
| `/quit` | Exit cleanly |

## How it works

- **UDP port 55000** — peer discovery and global messages
- **TCP port 55001** — direct messages
- **Threading** — all processes run simultaneously
- **JSON** — stores your username locally in `data/user.json`

## License

MIT
