import socket 
import threading
import time

HOST = "127.0.0.1"
PORT = 5000

MONITOR_HOST = "127.0.0.1"
MONITOR_PORT = 6000

def send_heartbeats():
    heartbeat_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        heartbeat_socket.sendto(
            b"HEARTBEAT",
            (MONITOR_HOST, MONITOR_PORT)
        )
        print("HEARTBEAT sent")
        time.sleep(1)
        

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Authentication service started...")
print(f"Listening on {HOST}:{PORT}")

heartbeat_thread = threading.Thread(
    target=send_heartbeats,
    daemon=True
)

heartbeat_thread.start()

while True:
    conn, addr = server.accept()
    print(f"Connection from {addr}")

    data = conn.recv(1024).decode()

    if data:
        print(f"Recieved: {data}")
        conn.sendall(b"Authentication request recieved")

    conn.close()
