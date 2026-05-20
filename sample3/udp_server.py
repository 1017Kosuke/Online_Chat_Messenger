import socket
import json

UDP_HOST = "127.0.0.1"
UDP_PORT = 9001

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.bind((UDP_HOST, UDP_PORT))

joined_users = {}
messages = []

print(f"UDP server is listening on {UDP_HOST}:{UDP_PORT}")


def create_response(status, message, history=None):
    response = {
        "status": status,
        "message": message
    }

    if history is not None:
        response["history"] = history

    return response


def get_payload(data):
    try:
        packet = json.loads(data.decode())
        return packet.get("payload", {}), None
    except json.JSONDecodeError:
        return None, "Invalid JSON"


def get_message_history(room_key):
    return [
        {
            "username": msg["username"],
            "message": msg["message"]
        }
        for msg in messages
        if msg["key"] == room_key
    ]


def handle_join(payload, client_address):
    key = payload.get("key")
    username = payload.get("username")

    if not key or not username:
        return create_response(
            "error",
            "JOIN requires key and username"
        )

    joined_users[client_address] = {
        "key": key,
        "username": username
    }

    return create_response(
        "success",
        f"{username} joined room {key}",
        get_message_history(key)
    )


def handle_message(payload):
    key = payload.get("key")
    username = payload.get("username")
    message = payload.get("message")

    if not key or not username or not message:
        return create_response(
            "error",
            "MESSAGE requires key, username, and message"
        )

    messages.append({
        "key": key,
        "username": username,
        "message": message
    })

    print(f"[{key}] {username}: {message}")

    return create_response(
        "success",
        f"Message received: {message}",
        get_message_history(key)
    )


def handle_get_history(payload):
    key = payload.get("key")

    if not key:
        return create_response(
            "error",
            "GET_HISTORY requires key"
        )

    return create_response(
        "success",
        "Message history fetched successfully",
        get_message_history(key)
    )


def handle_operation(payload, client_address):
    operation = payload.get("operation")

    if operation == "JOIN":
        return handle_join(payload, client_address)

    if operation == "MESSAGE":
        return handle_message(payload)

    if operation == "GET_HISTORY":
        return handle_get_history(payload)

    return create_response(
        "error",
        "Unknown UDP operation"
    )


while True:
    data, client_address = udp_sock.recvfrom(4096)

    payload, error = get_payload(data)

    if error:
        response = create_response("error", error)
    else:
        response = handle_operation(payload, client_address)

    udp_sock.sendto(
        json.dumps(response).encode(),
        client_address
    )