import socket
import datetime
import sys
import threading

HOST="0.0.0.0"
PORT=5000
BUFFER_SIZE=2048
MAX_CLIENTS=50

clients = {}
clients_lock = threading.Lock()

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
    
def broadcast(message : str): 
    with clients_lock:
        reciepents = list(clients.keys())
        for reciepent in reciepents:
            send_to(reciepent, message)
        
def get_client_name(client_socket : socket.socket) -> str:
    with clients_lock:
        info = clients.get(client_socket)
        return info["name"] if info else "Unknown"

def handle_client(client_socket : socket.socket , address : tuple):
    log(f"a new client connected with: {address}")

    send_to(client_socket, "hey welcome to the TCP chat server (By Bipanshu Kr)")
    send_to(client_socket, "enter your name : ")
    
    try:
        raw_name =  client_socket.recv(BUFFER_SIZE).decode().strip()
        
        name = (raw_name[:20] or "Guest").replace(" ", "-")  
        
        log(f" '{name}' joined with {address}")
        send_to(client_socket, f"\n you joined as {name}. say hello \n")
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
             
             thread = threading.Thread(
                 target=handle_client,
                 args=(client_socket, addr),
                 daemon=True
             )
             thread.start()
             
     except KeyboardInterrupt:
         log(f"shutting down server....")
         log(f"server closed cleanly")
         server_socket.close()
         sys.exit(0)        
     
     
if __name__ == "__main__":
    start_server()     