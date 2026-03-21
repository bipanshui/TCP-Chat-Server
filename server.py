import socket
import datetime
import sys

HOST="0.0.0.0"
PORT=5000
BUFFER_SIZE=2048
MAX_CLIENTS=50

clients = {}

def timestamp():
    return datetime.datetime.now().strftime("%H:%M:%S")

def log(message : str):
    print(f"[{timestamp()}] {message}")

def send_to(client_socket : socket.socket, message : str):
    try:
        msg = (message +" \n").encode()
        client_socket.sendall(msg)
    except:
        pass    

def handle_client(client_socket : socket.socket , address : tuple):
    log(f"a new client connected with: {address}")

    send_to(client_socket, "hey welcome to the TCP chat server (By Bipanshu Kr)")
    send_to(client_socket, "enter your name : ")
    
    try:
        raw_name =  client_socket.recv(BUFFER_SIZE).decode().strip()  
    except Exception:
        client_socket.close()
        return

def start_server():
     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      
     server_socket.bind((HOST, PORT))
     server_socket.listen(MAX_CLIENTS)
     
     log(f"╔═══════════════════════════════════════╗")
     log(f"║  PyChat Server started on port {PORT}   ║")
     log(f"║  Waiting for connections...           ║")
     log(f"╚═══════════════════════════════════════╝")
     log(f"  Connect via:  telnet localhost {PORT}")
     log(f"                nc localhost {PORT}")
     log(f"                python chat_client.py")
     
     try:
         while True:
             client_socket, addr = server_socket.accept()
             log(f"connected : {addr}")
             
             
     except KeyboardInterrupt:
         log(f"shutting down server....")
         log(f"server closed cleanly")
         
         sys.exit(0)        
     
     
if __name__ == "__main__":
    start_server()     