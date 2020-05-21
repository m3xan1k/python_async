import socket
import selectors


selector = selectors.DefaultSelector()


def server():
    HOST = '127.0.0.1'
    PORT = 5000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    # register socket into selectors
    selector.register(fileobj=server_socket, events=selectors.EVENT_READ,
                      data=accept_connection)


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()
    print(addr, 'connected')

    # register client socket
    selector.register(fileobj=client_socket, events=selectors.EVENT_READ,
                      data=send_message)


def send_message(client_socket):
    request = client_socket.recv(4096)
    if not request:
        print(client_socket, 'disconnected')
        selector.unregister(client_socket)
        client_socket.close()
    else:
        response = str(request).upper().encode()
        client_socket.send(response)


def event_loop():
    while True:
        events = selector.select()

        for key, _ in events:
            callback = key.data
            callback(key.fileobj)


if __name__ == '__main__':
    server()
    event_loop()
