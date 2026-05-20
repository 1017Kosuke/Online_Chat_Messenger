import socket
import json

from services.validation import validate_create_room
from services.room_service import password_writer


tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = "127.0.0.1"
server_port = 9000

tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_sock.bind((server_address, server_port))
tcp_sock.listen(1)


def start_tcp_server():
    print(f"TCP server is listening on {server_address}:{server_port}")

    while True:
        conn, client_address = tcp_sock.accept()
        print(f"Connection from {client_address}")

        try:
            raw_data = conn.recv(1024).decode()

            try:
                data = json.loads(raw_data)
            except json.JSONDecodeError:
                response = {
                    "status": "error",
                    "message": "Received data is not valid JSON"
                }
                conn.sendall(json.dumps(response).encode())
                conn.close()
                continue

            valid, error_message = validate_create_room(data)

            if not valid:
                response = {
                    "status": "error",
                    "message": error_message
                }
                conn.sendall(json.dumps(response).encode())
                conn.close()
                continue

            password_writer(
                data["room_name"],
                data["password"],
                data["key"]
            )

            response = {
                "status": "success",
                "message": "Room created successfully"
            }

            conn.sendall(json.dumps(response).encode())

        except Exception as e:
            print(f"Error: {e}")

        finally:
            conn.close()


if __name__ == "__main__":
    start_tcp_server()