import socket
import datetime

HOST="0.0.0.0"
PORT=5000
BUFFER_SIZE=2048
MAX_CLIENTS=50

def timestamp():
    return datetime.datetime.now().strftime("%H:%M:%S")

def log(message : str):
    print(f"[{timestamp()} {message}]")

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
     
     
if __name__ == "__main__":
    start_server()     