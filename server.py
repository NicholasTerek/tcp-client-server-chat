# Server.py - Step 5
import socket
import threading

HOST = '127.0.0.1'  # localhost
PORT = 5000 # Port to listen on
MAX_CLIENTS = 3 # Maximum number of clients

client_counter = 0
client_counter_lock = threading.Lock()

# To handle each client (runs in separate thread)
def handle_client(client_socket, client_address, client_name):
    print(f"[SERVER] Thread started for {client_name}")
    
    # Send client name
    client_socket.send(client_name.encode('utf-8'))
    print(f"[SERVER] Assigned name: {client_name}")
    
    # Message loop for this client
    while True:
        try:
            data = client_socket.recv(1024)
            
            if not data:
                print(f"[SERVER] {client_name} disconnected")
                break
            
            message = data.decode('utf-8')
            print(f"[SERVER] Received from {client_name}: '{message}'")
            
            if message.lower() == "exit":
                print(f"[SERVER] {client_name} requested exit")
                break
            
            response = message.upper()
            client_socket.send(response.encode('utf-8'))
            print(f"[SERVER] Sent to {client_name}: '{response}'")
            
        except Exception as e:
            print(f"[SERVER] Error with {client_name}: {e}")
            break
    
    client_socket.close()
    print(f"[SERVER] Connection with {client_name} closed")


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print(f"[SERVER] Socket created")

server_socket.bind((HOST, PORT))
print(f"[SERVER] Socket bound to {HOST}:{PORT}")

server_socket.listen(MAX_CLIENTS)
print(f"[SERVER] Server is listening for connections (max {MAX_CLIENTS} clients)...")

try:
    while True:
       
        client_socket, client_address = server_socket.accept()
        
        with client_counter_lock:
            client_counter += 1
            client_name = f"Client{client_counter:02d}"
        
        print(f"[SERVER] Connection accepted from {client_address}")
        
        client_thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address, client_name)
        )
        client_thread.start()
        
except KeyboardInterrupt:
    print("\n[SERVER] Server shutting down...")
finally:
    server_socket.close()
    print("[SERVER] Server socket closed")