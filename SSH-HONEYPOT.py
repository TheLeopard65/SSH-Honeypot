import paramiko
import socket
import logging
import os
import threading
import subprocess
from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')
log_filename = f"HONEYPOT-LOGS-{today}.log"
logging.basicConfig(filename=log_filename, level=logging.INFO, format="%(asctime)s - %(message)s")

IP_ADDRESS = '0.0.0.0'
SSH_PORT = 2222
VALID_USERS = { "kali": "kali", "admin": "password123", "root": "toor", "user1": "pass1", "guest": "guest123", }

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
        if username in VALID_USERS and VALID_USERS[username] == password:
	        logging.info(f"[!] SUCCESSFULL AUTHENTICATION ATTEMPT BY USER: {username}:{password} FROM IP: {client_ip} !!!")
	        print(f"[!] SUCCESSFULL AUTHENTICATION ATTEMPT BY USER: {username}:{password} FROM IP: {client_ip} !!!")
        	return paramiko.AUTH_SUCCESSFUL
        else:
	        logging.info(f"[!] FAILED AUTHENTICATION ATTEMPT BY USER: {username}:{password} FROM IP: {client_ip} !!!")
	        print(f"[!] FAILED AUTHENTICATION ATTEMPT BY USER: {username}:{password} FROM IP: {client_ip} !!!")
        	return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username): return 'password'
    def check_channel_pty_request( self, channel, term, width, height, pixelwidth, pixelheight, modes ): return True
    def check_channel_shell_request( self, channel ): return True

    def check_channel_request(self, channel_type, chanid):
        if channel_type in ['session', 'pty', 'shell']: return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def start_shell(self, channel):
        try:
            channel.get_pty()
            channel.send("[#] WELCOME TO THE SSH HONEYPOT! YOU ARE NOW IN A R-SHELL!\n")
            channel.invoke_shell()
        except Exception as error:
            logging.error(f"[@] ERROR (COULDN'T START REAL SHELL): {error}")
            channel.send(f"[@] ERROR (COULDN'T START REAL SHELL): {error}\n")
        finally:
            channel.close()

def handle_connection(client_sock, client_addr):
    try:
        client_ip = client_sock.getpeername()[0]
        transport = paramiko.Transport(client_sock)
        server_key = paramiko.RSAKey(filename='HONEYPOT-KEY')
        transport.add_server_key(server_key)
        ssh = SSHServer(client_sock.getpeername())
        transport.start_server(server=ssh)
        channel = transport.accept(15)
        if channel is None:
        	logging.error("[@] ERROR (CHHANEL IS NONE) : Connection may have Failed !!!")
        	print("[@] ERROR (CHHANEL IS NONE) : Connection may have Failed !!!")
        	return
        ssh.start_shell(channel)
    except Exception as error:
        logging.error(f"[@] ERROR (EXCEPTION IN HANDLE-CONNECTION FUNCTION): {error}")
        print(f"[@] ERROR (EXCEPTION IN HANDLE-CONNECTION FUNCTION): {error}")
    finally:
    	if transport and transport.is_active(): transport.close()
    	client_sock.close()

def start_server(host, port):
    print(f'[#] STARTING SSH HONEYPOT ON PORT : {port} !!!')
    logging.info(f'[#] STARTING SSH HONEYPOT ON PORT : {port} !!!')
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((host, port))
    server_sock.listen(16)
    while True:
        try:
            client_sock, client_addr = server_sock.accept()
            print(f"[#] CONNECTION RECEIVED FROM : ({client_addr[0]}:{client_addr[1]}) !!!")
            logging.info(f"[#] CONNECTION RECEIVED FROM : ({client_addr[0]}:{client_addr[1]}) !!!")
            client_thread = threading.Thread(target=handle_connection, args=(client_sock, client_addr))
            client_thread.start()
        except KeyboardInterrupt:
            print("[#] SHUTTING DOWN HONEYPOT -> RECEIVED KEYBOARD-INTERRUPT !!!")
            logging.info("[#] SHUTTING DOWN HONEYPOT -> RECEIVED KEYBOARD-INTERRUPT !!!")
            break
        except Exception as error:
            print(f"[@] ERROR (COULD ACCEPT CONNECTION) : {error}")
            logging.error(f"[@] ERROR (COULD ACCEPT CONNECTION) : {error}")

def main():
    try:
        generate_key()
        start_server(IP_ADDRESS, SSH_PORT)
    except Exception as error:
        logging.error(f"[@] ERROR (COULDN'T START SERVER) : {error}")
        print(f"[@] ERROR (COULDN'T START SERVER) : {error}")

if __name__ == '__main__':
    main()
