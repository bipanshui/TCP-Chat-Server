import socket 

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    socket_server.bind(('127.0.0.1', 8080))
    socket_server.listen()

    while True:
        client_socket, addr = socket_server.accept()
        print(client_socket)
except KeyboardInterrupt:
    pass
finally:
    socket_server.close()
