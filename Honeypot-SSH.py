import paramiko
import socket
import threading
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class SSHServer(paramiko.ServerInterface):
    def __init__(self, client_address):
        self.client_address = client_address
        super().__init__()

    def check_auth_password(self, username: str, password: str) -> int:
        client_ip = self.client_address[0]
        message = f"Authentication Attempt by: User {username} : Password: {password} from IP: {client_ip}"
        print(message)
        with open('honeypot.log', 'a') as log_file:
            log_file.write(message + '\n')
        if username == "Kali7986" and password == "KaliLinux7986450@?!":
            return paramiko.AUTH_SUCCESSFUL
        else:
            return paramiko.AUTH_FAILED

def handle_connection(client_sock):
    try:
        client_ip = client_sock.getpeername()[0]
        transport = paramiko.Transport(client_sock)
        server_key = paramiko.RSAKey(filename='key')
        transport.add_server_key(server_key)

        ssh = SSHServer(client_sock.getpeername())
        transport.start_server(server=ssh)

        transport.join()
    except Exception as e:
        print(f"Exception in handle_connection: {e}")
    finally:
        print("Connection handling completed.")

def start_honeypot(host, port):
    print(f'Starting honeypot on port {port}!')
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((host, port))
    server_sock.listen(223)

    while True:
        try:
            client_sock, client_addr = server_sock.accept()
            print(f"Connection from {client_addr[0]}:{client_addr[1]}")
            t = threading.Thread(target=handle_connection, args=(client_sock,))
            t.start()
        except KeyboardInterrupt:
            print("Received KeyboardInterrupt. Shutting down the honeypot.")
            break

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        message = f"Authentication Attempt by: User {username} : Password: {password} from IP: {request.remote_addr}"
        print(message)
        with open('honeypot.log', 'a') as log_file:
            log_file.write(message + '\n')
        return redirect(url_for('authenticate', username=username, password=password))
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form.get('username')
    password = request.form.get('password')
    message = f"Authentication Attempt by: User {username} : Password: {password} from IP: {request.remote_addr}"
    print(message)
    with open('honeypot.log', 'a') as log_file:
        log_file.write(message + '\n')

    if username == "Kali7986" and password == "KaliLinux7986450@?!":
        return render_template('dashboard.html', username=username)
    else:
        return render_template('authenticate.html')

def run_flask():
    app.run(host='0.0.0.0', port=80, debug=False, threaded=True)

def main():
    honeypot_thread = threading.Thread(target=start_honeypot, args=('localhost', 8080))
    honeypot_thread.start()

    try:
        run_flask()
    except KeyboardInterrupt:
        print("Received KeyboardInterrupt. Exiting...")
        honeypot_thread.join()

if __name__ == '__main__':
    main()
