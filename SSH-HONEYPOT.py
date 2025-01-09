import paramiko
import socket
import threading
import logging
import os
import subprocess
from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')
log_filename = f"HONEYPOT-LOGS-{today}.log"
logging.basicConfig(filename=log_filename, level=logging.INFO, format="%(asctime)s - %(message)s")

def generate_key():
    if not os.path.exists('HONEYPOT-KEY'):
        key = paramiko.RSAKey.generate(2048)
        key.write_private_key_file('HONEYPOT-KEY')

class SSHServer(paramiko.ServerInterface):
    def __init__(self, client_address):
        self.client_address = client_address
        super().__init__()

    def check_auth_password(self, username: str, password: str) -> int:
        client_ip = self.client_address[0]
        message = f"[!] AUTHENTICATION ATTEMPT BY USER: {username}:{password} FROM IP: {client_ip} !!!"
        logging.info(message)
        print(message)
        if username == "kali" and password == "kali": return paramiko.AUTH_SUCCESSFUL
        else: return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username): return 'password'

    def check_channel_request(self, channel_type, chanid):
        if channel_type == 'session': return paramiko.OPEN_SUCCEEDED
        elif channel_type == 'pty': return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def start_shell(self, channel):
        try:
            channel.send("[#] WELCOME TO THE SSH HONEYPOT SIMULATION!\n")
            process = subprocess.Popen(['/bin/sh'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
            while True:
                data = channel.recv(1024)
                if len(data) == 0: break
                process.stdin.write(data.decode())
                process.stdin.flush()
                output = process.stdout.read(1024)
                if len(output) > 0: channel.send(output)
                error = process.stderr.read(1024)
                if len(error) > 0: channel.send(error)
            process.stdin.close()
            process.stdout.close()
            process.stderr.close()
        except Exception as e:
            print(f"[@] ERROR (COULDN'T START SHELL): {e}")

def handle_connection(client_sock):
    try:
        client_ip = client_sock.getpeername()[0]
        transport = paramiko.Transport(client_sock)
        server_key = paramiko.RSAKey(filename='HONEYPOT-KEY')
        transport.add_server_key(server_key)
        ssh = SSHServer(client_sock.getpeername())
        transport.start_server(server=ssh)
        channel = transport.accept(15)
        if channel is None: return
        ssh.start_shell(channel)
    except Exception as e: print(f"[@] ERROR (EXCEPTION IN HANDLE-CONNECTION FUNCTION) : {e}")
    finally: pass

def start_honeypot(host, port):
    print(f'[#] STARTING SSH HONEYPOT ON PORT : {port} !!!')
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((host, port))
    server_sock.listen(16)
    while True:
        try:
            client_sock, client_addr = server_sock.accept()
            print(f"[#] CONNECTION RECEIVED FROM : ({client_addr[0]}:{client_addr[1]}) !!!")
            t = threading.Thread(target=handle_connection, args=(client_sock,))
            t.start()
        except KeyboardInterrupt:
            print("[#] SHUTTING DOWN HONEYPOT -> RECEIVED KEYBOARD-INTERRUPT !!!")
            break
        except Exception as e:
            print(f"[@] ERROR (COULD ACCEPT CONNECTION) : {e}")

def main():
    generate_key()
    honeypot_thread = threading.Thread(target=start_honeypot, args=('0.0.0.0', 2222))
    honeypot_thread.start()
    try: honeypot_thread.join()
    except KeyboardInterrupt: honeypot_thread.join()

if __name__ == '__main__':
    main()
