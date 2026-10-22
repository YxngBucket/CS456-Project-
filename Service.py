import socket 

HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Authentication service started...")
print(f"Listening on {HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    print(f"Connection from {addr}")

    data = conn.recv(1024).decode()

    if data:
        print(f"Recieved: {data}")
        conn.sendall(b"Authentication request recieved")

    conn.close()
