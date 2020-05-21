import socket
from select import select


HOST = '127.0.0.1'
PORT = 5000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)


# need to know items we are able to read
to_monitor = []


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()
    print(addr, 'connected')

    # need to watch client_socket ready for reading
    to_monitor.append(client_socket)


def send_message(client_socket):
    request = client_socket.recv(4096)
    if not request:
        print(client_socket, 'disconnected')
        client_socket.close()
        to_monitor.pop(to_monitor.index(client_socket))
    else:
        response = str(request).upper().encode()
        client_socket.send(response)


def event_loop():
    while True:

        # get sockets that are ready for reading(has data to read)
        if to_monitor:
            ready_to_read, _, _ = select(to_monitor, [], [])

        for sock in ready_to_read:
            if sock is server_socket:
                accept_connection(sock)
            else:
                send_message(sock)


if __name__ == '__main__':
    to_monitor.append(server_socket)
    event_loop()
