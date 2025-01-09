# Basic SSH-Honeypot: Introduction to Cybersecurity LAB Project (1st Semester 2023)

This repository contains a simple SSH honeypot implementation written in Python. The purpose of this honeypot is to simulate an SSH service that logs and handles authentication attempts and connection activities. It is designed to capture information about brute force attacks, username/password combinations used, and other malicious activities.

## Features

- **SSH Authentication Simulation:** The honeypot logs all SSH authentication attempts, including failed and successful login attempts.
- **SSH Session Simulation:** Once a successful authentication occurs, a fake shell is started, allowing attackers to interact with it.
- **Logging:** Logs of authentication attempts and session interactions are stored in a log file with the date included in the filename for easy tracking.
- **Customizable:** You can adjust the host, port, and SSH key handling as required.

## Setup

1. **Install Dependencies:**  
   Ensure you have the necessary Python dependencies installed. You can use the following command to install Paramiko:

   ```bash
   pip install paramiko
   ```

2. **Generate SSH Key:**  
   The first time the honeypot is run, it will generate an RSA key pair for SSH connections if one does not already exist. The key will be saved as `HONEYPOT-KEY` in the root directory.

3. **Running the Honeypot:**  
   To start the SSH honeypot, simply run the script:

   ```bash
   python SSH-HONEYPOT.py
   ```

   The honeypot will listen on all network interfaces (`0.0.0.0`) and port `2222` by default. You can change these values in the `start_honeypot` function.

4. **Log Files:**  
   All connection attempts are logged to a file named `HONEYPOT-LOGS-YYYY-MM-DD.log` (e.g., `HONEYPOT-LOGS-2025-01-09.log`).

## How It Works

- **SSH Key Generation:**  
  A 2048-bit RSA key is generated and saved to the `HONEYPOT-KEY` file if not already present.
  
- **Server Interface:**  
  The `SSHServer` class defines the behavior of the honeypot SSH server, handling authentication attempts and session management. If a user successfully logs in with the username "kali" and password "kali", a fake shell is spawned.
  
- **Connection Handling:**  
  The honeypot listens for incoming SSH connections on the specified host and port, spawning a new thread to handle each connection.

- **Logging:**  
  Every authentication attempt, along with the username, password, and IP address of the client, is logged to a date-specific file. The logs help track malicious activities and identify potential attack patterns.

## Files

- `SSH-HONEYPOT.py`: The main script that runs the honeypot server.
- `HONEYPOT-KEY`: The RSA private key used for SSH authentication.
- `LICENSE`: The license file for the project.
- `README.md`: This file, containing information about the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This honeypot is for educational and research purposes only. It should not be used in a production environment or for malicious activities. Always ensure you comply with applicable laws when setting up and using honeypots.

