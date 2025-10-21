import socket
import os

HOST = '127.0.0.1'
PORT = 5000
DOWNLOAD_FOLDER = 'client_downloads'

# Create download folder if it doesn't exist
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

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
    
    # Check if it's a file transfer
    try:
        response = data.decode('utf-8')
        if response.startswith("FILE:"):
            # Parse header: FILE:filename:size:
            parts = response.split(':', 3)
            if len(parts) >= 3:
                filename = parts[1]
                file_size = int(parts[2])
                
                # Receive file data
                file_data = b''
                remaining = file_size
                while remaining > 0:
                    chunk = client_socket.recv(min(8192, remaining))
                    if not chunk:
                        break
                    file_data += chunk
                    remaining -= len(chunk)
                
                # Save file
                filepath = os.path.join(DOWNLOAD_FOLDER, filename)
                with open(filepath, 'wb') as f:
                    f.write(file_data)
                print(f"[DOWNLOAD] File '{filename}' saved to {filepath} ({file_size} bytes)")
            else:
                print(response)
        else:
            print(response)
    except UnicodeDecodeError:
        # Binary data received without proper header
        print("[ERROR] Received binary data but couldn't parse file header")

client_socket.close()