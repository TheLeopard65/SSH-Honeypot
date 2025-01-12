# Basic SSH Honeypot: Introduction to Cybersecurity LAB Project (1st Semester 2023)

This repository contains a simple SSH honeypot implementation written in Python. The honeypot is designed to simulate an SSH service, capturing authentication attempts, handling connection activities, and monitoring potentially malicious behavior. It aims to gather insights into brute force attacks, credential guessing, and other unauthorized access attempts by interacting with attackers and logging their actions.

## Features

- **SSH Authentication Simulation:** Logs both successful and failed SSH login attempts.
- **PROVIDES rBASH SHELL** When a valid username and password are entered, the honeypot gives an interactive rbash shell, allowing attackers to attempt commands.
- **Real-Time Logging:** Logs all authentication attempts, including username/password combinations and IP addresses, in real-time with a timestamp for easy tracking. Creates seperate log file for each day.
- **Customizable Configuration:** The honeypot’s behavior, such as host, port, and SSH key handling, can be easily customized in the configuration section of the script.

## Setup

### 1. Install Dependencies

Make sure you have Python 3.7+ installed. The honeypot requires the `paramiko` library for handling SSH connections. Install it using the following command:

```bash
pip install paramiko
```

### 2. Generate SSH Key

The first time you run the honeypot, it will automatically generate an RSA key pair for SSH communication if one does not already exist. The private key is stored in the `HONEYPOT-KEY` file in the root directory.

### 3. Running the Honeypot

To start the honeypot, simply execute the `SSH-HONEYPOT.py` script:

```bash
python SSH-HONEYPOT.py
```

By default, the honeypot listens on all network interfaces (`0.0.0.0`) and port `2222`. You can change these settings in the script’s configuration section if needed.

### 4. Log Files

All connection attempts, both successful and failed, are logged to a file named `HONEYPOT-LOGS-YYYY-MM-DD.log`, where `YYYY-MM-DD` represents the current date. This log file includes details like:
- Authentication attempts
- Source IP address of the attacker
- Username/password used for login

Example filename: `HONEYPOT-LOGS-2025-01-09.log`.

## How It Works

### SSH Key Generation

Upon execution, if no private key is found, the script generates a 2048-bit RSA key pair and saves it as `HONEYPOT-KEY`. This key is used for SSH authentication in the honeypot.

### Server Interface

The core functionality of the honeypot is defined by the `SSHServer` class. It handles incoming SSH authentication attempts and spawns a rbash shell upon successful login. If a user provides a correct username and password (e.g., `kali:kali`, `root:toor`, `guest:guest123`, etc.), the system grants them access to a rbash shell.

### Connection Handling

The honeypot listens for incoming SSH connections on the specified IP and port. When a connection is received, the honeypot starts a new thread to handle the session, ensuring that multiple attackers can interact with the honeypot simultaneously.

### Logging

Each connection attempt is logged, including:
- The date and time of the attempt
- The username and password provided
- The IP address of the client attempting the login
- Commands Executed by the client in the rbash

This helps track potential attack patterns and provide valuable data for cybersecurity research.

## Files

- **`SSH-HONEYPOT.py`**: The main script that runs the SSH honeypot server.
- **`HONEYPOT-KEY`**: The RSA private key used for SSH authentication (generated automatically if not present).
- **`LICENSE`**: The license file for the project, specifying the terms under which the code can be used.
- **`README.md`**: This file, containing documentation and setup instructions.

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for full details.

## Disclaimer

This honeypot is intended for **educational and research purposes only**. It should not be used in production environments or for any malicious activities. Ensure that you comply with all applicable laws and regulations when setting up and using honeypots.
