# Server.py
import socket

HOST = '127.0.0.1'  # localhost
PORT = 5000 # Port to listen on
MAX_CLIENTS = 3 # Maximum number of clients
# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f"[SERVER] Socket created")

# Bind the socket to address and port
server_socket.bind((HOST, PORT))
print(f"[SERVER] Socket bound to {HOST}:{PORT}")

# Start listening for connections
server_socket.listen(MAX_CLIENTS) 
print(f"[SERVER] Server is listening for connections...")

client_socket, client_address = server_socket.accept()
print(f"[SERVER] Connection accepted from {client_address}")

# Close sockets
client_socket.close()
server_socket.close()
print(f"[SERVER] Server shut down")