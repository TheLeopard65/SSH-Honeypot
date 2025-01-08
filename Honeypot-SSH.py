import paramiko
import socket
import threading
import logging
import os
from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')
log_filename = f"HONEYPOT-{today}.log"
logging.basicConfig(filename=log_filename, level=logging.INFO, format="%(asctime)s - %(message)s")

def generate_key():
    if not os.path.exists('key'):
        key = paramiko.RSAKey.generate(2048)
        key.write_private_key_file('key')
        print("[#] RSA Key Generated and Saved to 'key'")

class SSHServer(paramiko.ServerInterface):
    def __init__(self, client_address):
        self.client_address = client_address
        super().__init__()

    def check_auth_password(self, username: str, password: str) -> int:
        client_ip = self.client_address[0]
        message = f"[!] AUTHENTICATION ATTEMPT BY USER : {username}:{password} FROM THE IP : {client_ip} !!!"
        logging.info(message)
        print(message)
        if username == "kali" and password == "Kali123":
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
    print(f'[#] STARTING HONEY-POT ON PORT : {port} !!!')
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((host, port))
    server_sock.listen(223)
    while True:
        try:
            client_sock, client_addr = server_sock.accept()
            print(f"[!] CONNECTION RECEIVED FROM {client_addr[0]}:{client_addr[1]} !!!")
            t = threading.Thread(target=handle_connection, args=(client_sock,))
            t.start()
        except KeyboardInterrupt:
            print("[#] SHUTTING DOWN HONEYPOT -> RECEIVED KEYBOARD-INTERRUPT !!!")
            break
        except Exception as e:
            print(f"Error while accepting a new connection: {e}")

def main():
    generate_key()
    honeypot_thread = threading.Thread(target=start_honeypot, args=('0.0.0.0', 2222))
    honeypot_thread.start()
    try:
        honeypot_thread.join()
    except KeyboardInterrupt:
        print("[@] EXITING SIMULATION -> RECEIVED KEYBOARD-INTERRUPT !!!")
        honeypot_thread.join()

if __name__ == '__main__':
    main()
