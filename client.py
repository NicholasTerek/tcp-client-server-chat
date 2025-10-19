# Client.py
import socket

HOST = '127.0.0.1'
PORT = 5000

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f"[CLIENT] Socket created")

# Connect to the server
client_socket.connect((HOST, PORT))
print(f"[CLIENT] Connected to server at {HOST}:{PORT}")

# Close the socket
client_socket.close()
print(f"[CLIENT] Disconnected from server")