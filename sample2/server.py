import socket
import os
import uuid
import threading

SERVER = '127.0.0.1'
PORT = 9050

dpath = './sample2/temp'
os.makedirs(dpath, exist_ok=True)

rooms = {}


def create_room(password, host_address):
    token = str(uuid.uuid4())
    os.mkdir(os.path.join(dpath, token))

    with open(os.path.join(dpath, token, "password.txt"), "w") as f:
        f.write(password)

    rooms[token] = {
        "members": {host_address}
    }

    return token

def verify_joint(room_name, password, addr, conn, token):
    if room_name not in rooms:
        conn.sendall("ERROR: Room does not exist".encode())
        return False

    with open(os.path.join(dpath, token, "password.txt"), "r") as f:
        correct_password = f.read()

    if password != correct_password:
        conn.sendall("ERROR: Incorrect password".encode())
        return False

    rooms[token]["members"].add(addr)
    return True


def handle_tcp():
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_sock.bind((SERVER, PORT))
    tcp_sock.listen(5)

    print("TCP server started")

    while True:
        conn, addr = tcp_sock.accept()
        print("TCP connected:", addr)

        data = conn.recv(4096)

        room_name_size = int.from_bytes(data[:1], "big")
        op = int.from_bytes(data[1:2], "big")
        payload_size = int.from_bytes(data[3:32], "big")

        body = data[32:]

        if op == 1:
            room_name = body[:room_name_size].decode()
            password = body[room_name_size:].decode()

            token = create_room(password, addr)

            conn.sendall(f"OK TOKEN:{token}".encode())
        elif op == 2:
            room_name = body[:room_name_size].decode()
            password = body[room_name_size:].decode()
            token = body[room_name_size:room_name_size + payload_size].decode()


            if(verify_joint(room_name, password, addr, conn, token)):
                print(f"{addr} joined room {room_name}")
                conn.sendall("OK".encode())

            else:
                print(f"{addr} failed to join room {room_name}")
        else:
            conn.sendall("ERROR: Invalid operation".encode())

        conn.close()


def handle_udp():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind((SERVER, PORT))

    print("UDP server started")

    while True:
        data, addr = udp_sock.recvfrom(4096)

        token_size = data[1]
        token = data[2:2 + token_size].decode()
        message = data[2 + token_size:].decode()

        print(f"[{token}] {addr}: {message}")

        if token not in rooms:
            continue

        for user in rooms[token]["members"]:
            if user != addr:
                udp_sock.sendto(data, user)


def main():
    threading.Thread(target=handle_tcp, daemon=True).start()
    handle_udp()


if __name__ == "__main__":
    main()