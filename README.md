
_**This was my First Semester Project 2023 for Introduction to Cybersecurity LAB**_

_**# SSH-Server-Basic-Honeypot**_
  This Python code sets up a basic honeypot using Flask and Paramiko. It logs SSH and web login attempts, providing insights into potential security threats. The code is an educational example, demonstrating how to detect and log unauthorized access for learning cybersecurity concepts.

**SIMPLE EXPLANATION:**
  This Python code implements a simple honeypot system using the Flask web framework and Paramiko library. A honeypot is a security mechanism set to detect, deflect, or, in this case, log attempts at unauthorized use of information systems. Here's a breakdown:

**SSH Honeypot:**
  It creates an SSH server using Paramiko that logs authentication attempts.
  It checks the provided username and password, logging details of each attempt in a file ('honeypot.log').
  If the provided credentials match a predefined set ("Kali7986" and "KaliLinux7986450@?!"), the authentication is considered successful; otherwise, it fails.

**Web Interface (Flask):**
  It provides a simple web interface with a login page.
  When users attempt to log in via the web form, their credentials are logged similarly to the SSH attempts.
  If the provided credentials match the predefined set, it redirects to a dashboard; otherwise, it shows an authentication failure page.

**Running Concurrently:**
  The SSH honeypot and the Flask web server run concurrently in separate threads.
  The Flask server runs on port 80, while the SSH honeypot runs on port 8080.

  **DETAILED EXPLANATION:**

**SSH Honeypot (SSHServer class and related functions):**
  The SSHServer class extends paramiko.ServerInterface to handle SSH authentication.
It overrides the check_auth_password method to log authentication attempts and accept or reject based on predefined credentials.
The handle_connection function sets up an SSH server on a separate thread for each incoming connection.
It uses the paramiko.Transport to handle SSH transport and authentication, and logs attempts to the 'honeypot.log' file.

**Flask Web Interface (Flask app and related routes):**
  The Flask web app has three routes: '/' (redirects to '/login'), '/login', and '/authenticate'.
The '/' route redirects to the login page, and the '/login' route renders the login form or handles the form submission.
The form data is logged, and if the credentials match the predefined set, it redirects to the dashboard; otherwise, it shows an authentication failure page.

**Running the Application (main function and related functions):**
  The start_honeypot function sets up a socket to listen for incoming connections on port 8080 and spawns a new thread for each connection.
The Flask web server runs in the main thread on port 80 using the run_flask function.
The main function starts the SSH honeypot in a separate thread and runs the Flask server in the main thread.

**Interrupt Handling:**
The application handles a KeyboardInterrupt gracefully, printing a message and waiting for the SSH honeypot thread to finish before exiting.
**_EXECUTION:_**

The script is configured to run both the SSH honeypot and the Flask web server concurrently, creating a honeypot environment for SSH and web login attempts.
This application serves as an educational example of setting up a basic honeypot system to understand and analyze potential security threats. It is crucial to note that deploying honeypots in real-world scenarios requires careful consideration of legal and ethical aspects.

_**HOW TO USE:**_
  Start the code in the VScode or the Python IDLE, it will open up a new terminal showing that Honeypot has startted on 8080. (You can modify the port in code). The site is live if someones tries to login their creadentials and IP will be captured.
