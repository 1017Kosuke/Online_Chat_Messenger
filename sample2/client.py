import socket
import sys

def tcp_protocol_header(RoomNameSize, Operation, State, OperationPayloadSize):
    return (
        RoomNameSize.to_bytes(1, "big") +
        Operation.to_bytes(1, "big") +
        State.to_bytes(1, "big") +
        OperationPayloadSize.to_bytes(29, "big")
    )

def udp_protocol_header(RoomNameSize, TokenSize):
    return (
        RoomNameSize.to_bytes(1, "big") +
        TokenSize.to_bytes(1, "big")
    )

tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = input("Server IP: ")
server_port = 9050

print(f'connecting to {server_address}: {server_port}')

try:
    tcp_sock.connect((server_address, server_port))
except socket.error as err:
    print(err)
    sys.exit(1)

try:
    Operation = int(input(
        'Operation:'
        '(1 for create room, 2 for join room): '
    ))

    RoomName = input('Room name: ')
    if(Operation == 2):
        RoomToken = input('Room token: ')
        token_bits = RoomToken.encode('utf-8')

    RoomPassword = input('Room password: ')

    RoomName_Bits = RoomName.encode('utf-8')
    RoomPassword_Bits = RoomPassword.encode('utf-8')

    header = tcp_protocol_header(
        len(RoomName_Bits),
        Operation,
        len(token_bits) if Operation == 2 else 0,
        len(RoomPassword_Bits)
    )

    tcp_sock.sendall(header + RoomName_Bits + token_bits + RoomPassword_Bits)

    data = tcp_sock.recv(4096).decode()
    print("SERVER:", data)

    if data.startswith("OK"):
        RoomToken = data.split("TOKEN:")[1].strip()
        Token_Bits = RoomToken.encode('utf-8')

        print("Your token:", RoomToken)

    while True:
        message = input("Message: ")

        msg_bits = message.encode('utf-8')

        header = udp_protocol_header(0, len(Token_Bits))

        packet = header + Token_Bits + msg_bits

        udp_sock.sendto(packet, (server_address, server_port))

        print('waiting...')
        data, _ = udp_sock.recvfrom(4096)

        print('received:', data.decode())

finally:
    print('closing socket')
    tcp_sock.close()
    udp_sock.close()