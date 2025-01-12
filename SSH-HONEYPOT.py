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
            self.username = username
            logging.info(f"[!] SUCCESSFUL AUTHENTICATION ATTEMPT BY USER: {username}:{password} FROM IP: {client_ip} !!!")
            print(f"[!] SUCCESSFUL AUTHENTICATION ATTEMPT BY USER: {username}:{password} FROM IP: {client_ip} !!!")
            return paramiko.AUTH_SUCCESSFUL
        else:
            logging.info(f"[!] FAILED AUTHENTICATION ATTEMPT BY USER: {username}:{password} FROM IP: {client_ip} !!!")
            print(f"[!] FAILED AUTHENTICATION ATTEMPT BY USER: {username}:{password} FROM IP: {client_ip} !!!")
            return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username): return 'password'
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes): return True
    def check_channel_shell_request(self, channel): return True

    def check_channel_request(self, channel_type, chanid):
        if channel_type in ['session', 'pty']: return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def start_shell(self, channel):
        try:
            channel.send("[#] WELCOME TO THE SSH HONEYPOT! YOU ARE NOW IN A R-SHELL!\n")
            process = subprocess.Popen('/bin/rbash', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
            while True:
                if not channel.active: break
                channel.send(f"\r{self.username}@system:~$ ")
                command = ""
                while True:
                    char = channel.recv(1).decode()
                    if (not char) or (char == '\r') or (char == '\x03') or (char == '\x04'): break
                    command += char
                    channel.send(char)
                command = command.strip()
                if (command == 'exit') or (command == '^C'): break
                try:
                    process = subprocess.Popen(['/bin/rbash', '-c', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = process.communicate()
                    if stdout: channel.send(f"\r\n{stdout.decode()}")
                    if stderr: channel.send(f"\r\n{stderr.decode()}")
                    if not stdout and not stderr: channel.send(f"\r\nERROR#: COMMAND {command} DID NOT PRODUCE ANY OUTPUT OR WAS INVALID !!!\n")
                except Exception as error:
                    channel.send(f"\r\nERROR#: Exception occurred while executing command: {str(error)}\n")
        except Exception as error:
            logging.error(f"[@] ERROR (COULDN'T START R-SHELL): {error}")
            if channel.active: channel.send(f"[@] ERROR (COULDN'T START R-SHELL): {error}\n")
            print(f"[@] ERROR (COULDN'T START R-SHELL): {error}\n")
        finally:
            if channel.active: channel.close()

def handle_connection(client_sock, client_addr):
    try:
        client_ip = client_sock.getpeername()[0]
        transport = paramiko.Transport(client_sock)
        server_key = paramiko.RSAKey(filename='HONEYPOT-KEY')
        transport.add_server_key(server_key)
        ssh = SSHServer(client_sock.getpeername())
        transport.start_server(server=ssh)
        channel = transport.accept(25)
        if channel is None:
            logging.error("[@] ERROR (CHANNEL IS NONE): Connection may have failed !!!")
            print("[@] ERROR (CHANNEL IS NONE): Connection may have failed !!!")
            return
        ssh.start_shell(channel)
    except socket.error as e:
        logging.error(f"[@] ERROR (SOCKET ERROR): {e}")
        print(f"[@] ERROR (SOCKET ERROR): {e}")
    except Exception as error:
        logging.error(f"[@] ERROR (EXCEPTION IN HANDLE-CONNECTION FUNCTION): {error}")
        print(f"[@] ERROR (EXCEPTION IN HANDLE-CONNECTION FUNCTION): {error}")
    finally:
        if transport.is_active(): transport.close()
        client_sock.close()

def start_server(host, port):
    print(f'[#] STARTING SSH HONEYPOT ON PORT : {port} !!!')
    logging.info(f'[#] STARTING SSH HONEYPOT ON PORT : {port} !!!')
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((host, port))
    server_sock.listen(16)
    try:
        while True:
            try:
                client_sock, client_addr = server_sock.accept()
                print(f"[#] CONNECTION RECEIVED FROM : ({client_addr[0]}:{client_addr[1]}) !!!")
                logging.info(f"[#] CONNECTION RECEIVED FROM : ({client_addr[0]}:{client_addr[1]}) !!!")
                client_thread = threading.Thread(target=handle_connection, args=(client_sock, client_addr))
                client_thread.start()
            except socket.error as error:
                print(f"[@] ERROR (COULD ACCEPT CONNECTION): {error}")
                logging.error(f"[@] ERROR (COULD ACCEPT CONNECTION): {error}")
            except Exception as e:
                print(f"[@] ERROR (UNEXPECTED ERROR): {e}")
                logging.error(f"[@] ERROR (UNEXPECTED ERROR): {e}")
    except KeyboardInterrupt:
        print("[#] SHUTTING DOWN HONEYPOT -> RECEIVED KEYBOARD-INTERRUPT !!!")
        logging.info("[#] SHUTTING DOWN HONEYPOT -> RECEIVED KEYBOARD-INTERRUPT !!!")
    finally:
        server_sock.close()

def main():
    try:
        generate_key()
        start_server(IP_ADDRESS, SSH_PORT)
    except Exception as error:
        logging.error(f"[@] ERROR (COULDN'T START SERVER): {error}")
        print(f"[@] ERROR (COULDN'T START SERVER): {error}")
    except KeyboardInterrupt:
        print("[#] SERVER SHUTDOWN GRACEFULLY DUE TO KEYBOARD INTERRUPT.")
        logging.info("[#] SERVER SHUTDOWN GRACEFULLY DUE TO KEYBOARD INTERRUPT.")

if __name__ == '__main__':
    main()
