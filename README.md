# SSH Server Basic Honeypot: Introduction to Cybersecurity LAB Project (First Semester 2023)

## Overview

This Python project serves as an introductory exploration into the realm of cybersecurity by implementing a basic honeypot system. The focus is on logging SSH and web login attempts, offering insights into potential security threats. The code is designed as an educational example to illustrate the detection and logging of unauthorized access, enhancing understanding of cybersecurity concepts.

## Project Components

### SSH Honeypot

The SSH honeypot component utilizes Paramiko to create an SSH server that logs authentication attempts. It scrutinizes provided usernames and passwords, logging details of each attempt into a file named 'honeypot.log'. Successful authentication is determined by matching the credentials against a predefined set ("Kali7986" and "KaliLinux7986450@?!").

### Web Interface (Flask)

The project incorporates a [Flask](https://flask.palletsprojects.com/) web framework to provide a user-friendly interface. A simple web page with a login form captures user credentials. Similar to the SSH honeypot, unsuccessful login attempts are logged, and if the provided credentials match the predefined set, the user is redirected to a dashboard; otherwise, an authentication failure page is displayed.

### Concurrent Execution

Both the SSH honeypot and the Flask web server run concurrently in separate threads. The Flask server operates on port 80, while the SSH honeypot runs on port 8080.

## Detailed Explanation

### SSH Honeypot (SSHServer Class)

The SSHServer class, extending `paramiko.ServerInterface`, manages SSH authentication. It overrides the `check_auth_password` method to log attempts and accept or reject based on predefined credentials. The `handle_connection` function sets up an SSH server on a separate thread for each incoming connection using `paramiko.Transport`, logging attempts to 'honeypot.log'.

### Flask Web Interface

The Flask web app has three routes: '/', '/login', and '/authenticate'. The former redirects to the login page, the second handles the login form, and the latter manages authentication. Form data is logged, and successful logins redirect to the dashboard.

### Running the Application

The `start_honeypot` function initiates a socket to listen for connections on port 8080, creating a new thread for each connection. The `run_flask` function runs the Flask server in the main thread on port 80. The main function starts the SSH honeypot in a separate thread.

### Interrupt Handling

The application gracefully handles a `KeyboardInterrupt`, printing a message and waiting for the SSH honeypot thread to finish before exiting.

## Execution

To run the application, execute the script in VScode or Python IDLE. It opens a new terminal indicating the honeypot has started on port 8080. The live site captures credentials and IP addresses when login attempts are made.

## How to Use

1. **Start the Code:** Run the script in VScode or Python IDLE.
2. **Access Honeypot:** The terminal will indicate the honeypot's initiation on port 8080 (you can modify the port in the code).
3. **Live Monitoring:** The site is live, capturing credentials and IP addresses upon login attempts. Note: Careful consideration of legal and ethical aspects is crucial when deploying honeypots in real-world scenarios.
