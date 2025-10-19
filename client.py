import socket

HOST = '127.0.0.1'
PORT = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Receive name or rejection
data = client_socket.recv(1024)
response = data.decode('utf-8')

if "Server is full" in response:
    print(f"[CLIENT] {response}")
    client_socket.close()
    exit()

client_name = response
print(f"[CLIENT] Assigned: {client_name}")

while True:
    message = input(f"{client_name}> ")
    client_socket.send(message.encode('utf-8'))
    
    if message.lower() == "exit":
        print(f"[{client_name}] Goodbye!")
        break
    
    # Receive response
    data = client_socket.recv(8192)
    response = data.decode('utf-8')
    print(response)

client_socket.close()