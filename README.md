# HarpiaC2 - Brazilian Command and Control Framework 🦅

This repository contains a Python-based proof of concept (PoC) for a lightweight and stealthy Command and Control (C2) framework named **HarpiaC2**.

It demonstrates how a bot client can connect to a central operator (C2 server), receive remote shell commands, execute them on the infected machine, and return the output securely.

---

## Concept

**HarpiaC2** simulates a real-world **Command and Control** scenario — typically used in **Red Team operations** and **botnet control structures**. Bots (clients) connect to the C2 server and await instructions.

- The **server** listens for incoming bot connections.
- The **bot client** connects, authenticates via a secure key exchange, and awaits OS-level commands.

Once connected, operators can interact with bots, execute shell commands remotely, and receive results in real time.

---

## Preview

![HarpiaC2 running](assets/image/print_screen_terminal.png)

The screenshot shows:
- Left: C2 operator issuing commands
- Right: Bot client executing and returning the result

---

## 🧰 Technologies Used

- Python 3.x
- Socket Programming (`socket`)
- Command Execution (`subprocess`)
- Secure AES Encryption with DH Key Exchange (`cryptography`)
- ANSI Coloring with `colorama`

---

## Project Structure

```bash
HarpiaC2/
├── multi_c2_server.py       # Main C2 controller (multi-bot)
├── bot_client.py            # Bot implant/client
├── c2_console.py            # Legacy console (single bot mode)
├── modules/
│   └── commands.py          # System info and command execution
├── utils/
│   ├── aes_crypto.py        # AES encryption layer
│   ├── key_exchange.py      # Diffie-Hellman key exchange
│   └── helpers.py           # Banners, logging, utils
├── assets/
│   └── image/
│       └── print_screen_terminal.png
├── logs/                    # Command logs per bot
├── .gitignore
└── README.md
```

---

## How to Use

### 1. Start the Server
Open a terminal and run:
```bash
python multi_c2_server.py
```

### 2. Deploy a Bot Client
On another machine or terminal, run:
```bash
python bot_client.py
```

The bot will connect automatically, perform key exchange, and await commands.

---

## Features

- Multi-bot connection support ✅
- Encrypted communication (AES/DH) ✅
- Command execution with output ✅
- Terminal logging by bot ✅
- Persistent installation option ✅
- Easy to expand and customize ✅

---

© 2025 – Igor | Projeto HarpiaC2 🦅
