# python server.py

import socket
import threading
import os
import time
import sys
from datetime import datetime

HOST = '127.0.0.1'
PORT = 5000
MAX_CLIENTS = 3
FILE_REPO = 'server_files'

# Tracking
client_counter = 0
active_clients = 0
client_cache = []
lock = threading.Lock()

def handle_client(client_socket, client_address, client_name):
    global active_clients
    
    # Add to cache
    connect_time = datetime.now()
    client_info = {'name': client_name, 'address': client_address, 
                   'connected': connect_time, 'disconnected': None}
    with lock:
        client_cache.append(client_info)
    
    # Send client name
    client_socket.send(client_name.encode('utf-8'))
    print(f"[SERVER] {client_name} connected from {client_address}")
    
    # Message loop
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        
        message = data.decode('utf-8').strip()
        print(f"[SERVER] {client_name}: {message}")
        
        if message.lower() == "exit":
            break
        
        elif message.lower() == "status":
            # Send cache
            status = "\n===== CLIENT CACHE =====\n"
            with lock:
                for c in client_cache:
                    status += f"{c['name']} | {c['address']} | "
                    status += f"Connected: {c['connected'].strftime('%H:%M:%S')} | "
                    status += f"Disconnected: {c['disconnected'].strftime('%H:%M:%S') if c['disconnected'] else 'ACTIVE'}\n"
            client_socket.send(status.encode('utf-8'))
        
        elif message.lower() == "list":
            # Send file list
            try:
                files = os.listdir(FILE_REPO)
                file_list = "Files: " + ", ".join(files) if files else "No files available"
                client_socket.send(file_list.encode('utf-8'))
            except:
                client_socket.send("Error: Repository not found".encode('utf-8'))
        
        elif message.lower().startswith("file "):
            # File request command: "file filename.txt"
            filename = message[5:].strip()
            filepath = os.path.join(FILE_REPO, filename)
            
            if os.path.isfile(filepath):
                # Send file size first, then file data
                file_size = os.path.getsize(filepath)
                header = f"FILE:{filename}:{file_size}:"
                client_socket.send(header.encode('utf-8'))
                
                # Wait a bit for client to process header
                time.sleep(0.1)
                
                # Send file data
                with open(filepath, 'rb') as f:
                    file_data = f.read()
                client_socket.send(file_data)
                print(f"[SERVER] Sent file '{filename}' ({file_size} bytes) to {client_name}")
            else:
                error_msg = f"Error: File '{filename}' not found"
                client_socket.send(error_msg.encode('utf-8'))
        
        else:
            # Regular message - send ACK
            response = message + " ACK"
            client_socket.send(response.encode('utf-8'))
    
    # Update cache and cleanup
    with lock:
        for c in client_cache:
            if c['name'] == client_name and not c['disconnected']:
                c['disconnected'] = datetime.now()
        active_clients -= 1
    
    client_socket.close()
    print(f"[SERVER] {client_name} disconnected. Active: {active_clients}/{MAX_CLIENTS}")

# Create file repository if it doesn't exist
if not os.path.exists(FILE_REPO):
    os.makedirs(FILE_REPO)
    # Create sample files
    with open(os.path.join(FILE_REPO, 'sample1.txt'), 'w') as f:
        f.write("This is sample file 1")
    with open(os.path.join(FILE_REPO, 'sample2.txt'), 'w') as f:
        f.write("This is sample file 2")

# Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.settimeout(1.0)  # 1 second timeout to allow Ctrl+C to work
server_socket.bind((HOST, PORT))
server_socket.listen(MAX_CLIENTS)
print(f"[SERVER] Listening on {HOST}:{PORT} (max {MAX_CLIENTS} clients)")

try:
    while True:
        try:
            client_socket, client_address = server_socket.accept()
        except socket.timeout:
            continue
        
        # Check capacity
        with lock:
            if active_clients >= MAX_CLIENTS:
                print(f"[SERVER] Rejected {client_address} - server full")
                client_socket.send("Server is full. Try again later.".encode('utf-8'))
                client_socket.close()
                continue
            
            active_clients += 1
            client_counter += 1
            client_name = f"Client{client_counter:02d}"
        
        print(f"[SERVER] Accepted connection. Active: {active_clients}/{MAX_CLIENTS}")
        
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address, client_name))
        thread.start()

except KeyboardInterrupt:
    print("\n[SERVER] Shutting down")
    server_socket.close()
    sys.exit(0)