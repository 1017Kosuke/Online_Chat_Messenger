import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = input('Enter server IP address: ').strip()
server_port = 12345
port = 9050
usernamelen = 255

try:
    while True:
        print('\nWaiting to send message')
        name = input('Enter your name: ')
        message = input('Enter your message: ')

        name_bytes = name.encode('utf-8')
        if len(name_bytes) > usernamelen:
            name_bytes = name_bytes[:usernamelen]
        else:
            name_bytes = name_bytes.ljust(usernamelen, b' ')

        message_bytes = message.encode('utf-8')

        data = name_bytes + message_bytes

        sent = sock.sendto(data, (server_address, server_port))
        print('Sent {} bytes to {}'.format(sent, (server_address, server_port)))

        data, server = sock.recvfrom(4096)
        name_received = data[:usernamelen].decode('utf-8').strip()
        message_received = data[usernamelen:].decode('utf-8').strip()
        print('Name: {}, Message: {}'.format(name_received, message_received))

except KeyboardInterrupt:
    print('\nClosing socket')
    sock.close()