import socket
import datetime
import sys
import threading
from typing import Optional

HOST="0.0.0.0"
PORT=5000
BUFFER_SIZE=2048
MAX_CLIENTS=50

clients = {}
clients_lock = threading.Lock()

def timestamp():
    return datetime.datetime.now().strftime("%H:%M:%S")

def log(message : str):
    print(f"[{timestamp()}] {message}", flush=True)

def send_to(client_socket : socket.socket, message : str):
    try:
        msg = (message +" \n").encode()
        client_socket.sendall(msg)
    except:
        pass    
    
def broadcast(message : str, exclude_socket : Optional[socket.socket] = None):
    
    with clients_lock:
        reciepents = list(clients.keys())
    
    for client_socket in reciepents:
        if client_socket is not exclude_socket:
            send_to(client_socket, message)             
        
def get_client_name(client_socket : socket.socket) -> str:
    with clients_lock:
        info = clients.get(client_socket)
        return info["name"] if info else "Unknown"

def recv_lines(client_socket: socket.socket, buffer: str):
    data = client_socket.recv(BUFFER_SIZE)
    if not data:
        return [], buffer, False

    buffer += data.decode(errors="replace")
    lines = []

    while "\n" in buffer:
        line, buffer = buffer.split("\n", 1)
        lines.append(line.rstrip("\r"))

    return lines, buffer, True

def handle_client(client_socket : socket.socket , address : tuple):
    log(f"a new client connected with: {address}")

    send_to(client_socket, "hey welcome to the TCP chat server (By Bipanshu Kr)")
    send_to(client_socket, "enter your name : ")

    pending_buffer = ""
    try:
        name_lines = []
        while not name_lines:
            name_lines, pending_buffer, connected = recv_lines(client_socket, pending_buffer)
            if not connected:
                client_socket.close()
                return
    except Exception:
        client_socket.close()
        return

    raw_name = name_lines.pop(0).strip()
    pending_lines = name_lines
    name = (raw_name[:20] or "Guest").replace(" ", "-")
    with clients_lock:
        existing = [info["name"] for info in clients.values()]
    if name in existing:
        name = f"{name}_{len(existing)}"    
        
    with clients_lock:
        time = timestamp()
        clients[client_socket] = {
            "name" : name,
            "addr" : address,
            "joined" : time 
        }  
    
    log(f"{clients[client_socket]}")   
    log(f"'{name}' joined ({address})")
    send_to(client_socket, f"you joined as {name}")    

    with clients_lock:
        count = len(clients)

    broadcast(f"{name} joined the server [online = {count}]", client_socket)
    
    try:
        while True:
             lines = pending_lines
             pending_lines = []

             if not lines and pending_buffer:
                 if "\n" in pending_buffer:
                     lines = pending_buffer.split("\n")
                     pending_buffer = lines.pop()
                     lines = [line.rstrip("\r") for line in lines]
                 else:
                     lines, pending_buffer, connected = recv_lines(client_socket, pending_buffer)
                     if not connected:
                         break
             elif not lines:
                 lines, pending_buffer, connected = recv_lines(client_socket, pending_buffer)
                 if not connected:
                     break

             for raw_line in lines:
                 message = raw_line.strip()
                 if not message:
                     log(f"can't get the message from {name}")
                     continue

                 if message.lower() == "/quit":
                     send_to(client_socket, "Good bye....")
                     return

                 log(f"'{name}' : {message}")
                 broadcast(f"{name}: {message}", client_socket)
    except ConnectionResetError:
        log(f" '{name}' disconnected abruptly")
        
    except Exception as e :
        log(f" Error with '{name}' : {e}")
        
    finally:
        with clients_lock:
            clients.pop(client_socket, None)
            remaining = len(clients)
        client_socket.close()
        log(f"'{name}' left ({remaining} users online)") 
        broadcast(f" '{name}' left the chat ({remaining} users remaining)")
        
                                
def start_server():
     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      
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
     finally:
         server_socket.close()
         log(f"server closed cleanly")
         sys.exit(0)        
     
     
if __name__ == "__main__":
    start_server()     
