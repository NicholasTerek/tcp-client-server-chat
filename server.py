# Server.py
import socket

HOST = '127.0.0.1'  # localhost
PORT = 5000 # Port to listen on
MAX_CLIENTS = 3 # Maximum number of clients
client_counter = 0

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f"[SERVER] Socket created")

# Bind the socket to address and port
server_socket.bind((HOST, PORT))
print(f"[SERVER] Socket bound to {HOST}:{PORT}")

server_socket.listen(MAX_CLIENTS) 
print(f"[SERVER] Server is listening for connections...")

client_counter += 1
client_name = f"Client{client_counter:02d}"

client_socket, client_address = server_socket.accept()
print(f"[SERVER] Connection accepted from {client_address}")

client_socket.send(client_name.encode('utf-8'))
print(f"[SERVER] Assigned name: {client_name}")
while True:
    
    data = client_socket.recv(1024)
    if not data:
        print(f"[SERVER] Client disconnected")
        break

    message = data.decode('utf-8')
    print(f"[SERVER] Received message: '{message}'")

    response = message.upper()
    client_socket.send(response.encode('utf-8'))
    print(f"[SERVER] Sent response: '{response}'")

    if message.lower() == "exit":
        print(f"[SERVER] Client requested exit")
        break

# Close sockets
client_socket.close()
server_socket.close()
print(f"[SERVER] Server shut down")