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

data = client_socket.recv(1024)
client_name = data.decode('utf-8')
print(f"[CLIENT] Server assigned name: {client_name}")

while True:
    message = input(f"{client_name}> ")

    if message.lower() == "exit":
        break

    client_socket.send(message.encode('utf-8'))
    print(f"[CLIENT] Sent message: '{message}'")

    data = client_socket.recv(1024)
    response = data.decode('utf-8')
    print(f"[CLIENT] Received response: '{response}'")


# Close the socket
client_socket.close()
print(f"[CLIENT] Disconnected from server")
response = data.decode('utf-8')
print(f"[CLIENT] Received response: '{response}'")
# Close the socket
client_socket.close()
print(f"[CLIENT] Disconnected from server")