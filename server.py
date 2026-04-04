import socket
import os
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = '127.0.0.1'
server_port = 12345
usernamelen = 255

dpath = 'temp'

if not os.path.exists(dpath):
    os.makedirs(dpath)

print('Starting up on {} port {}'.format(server_address, server_port))

sock.bind((server_address, server_port))

clients = {}

while True:
    print('\nWaiting to receive message')
    try:
        data, address = sock.recvfrom(4096)      

        ip, port = address
        name = data[:usernamelen].decode('utf-8').strip()
        message = str(data[usernamelen:].decode('utf-8').strip())

        print('Received {} bytes from {}'.format(len(data), address))
        print('Name: {}, Message: {}'.format(name, message))

        clients[address] = {
            'username': name,
            'last_seen': time.time()
        }

        for client_address in clients:
            if client_address != address:
                sent = sock.sendto(data, client_address)
                print('Sent {} bytes to {}'.format(sent, client_address))

        now = time.time()

        for client_address in list(clients.keys()):
            last_seen = clients[client_address]['last_seen']
            if now - last_seen > 300:
                print('Removing inactive client: {}'.format(client_address))
                del clients[client_address]

    except KeyboardInterrupt:
        print('\nClosing socket')
        sock.close()
        break