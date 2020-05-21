import socket


def main():
    HOST = '127.0.0.1'
    PORT = 5000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    while True:
        print('Enter first loop')
        client_socket, addr = server_socket.accept()
        print(addr, 'connected ')

        while True:
            request = client_socket.recv(4096)
            if not request:
                break
            response = str(request).upper().encode()
            client_socket.send(response)
        print('Outside nested while')
        client_socket.close()


if __name__ == '__main__':
    main()
