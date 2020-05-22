import socket
from select import select


to_read = {}
to_write = {}
tasks = []


def server():
    HOST = '127.0.0.1'
    PORT = 5000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    while True:
        yield ('read', server_socket)
        client_socket, addr = server_socket.accept()

        print(addr, 'connected ')
        tasks.append(client(client_socket))


def client(client_socket):
    while True:

        yield ('read', client_socket)
        request = client_socket.recv(4096)

        if not request:
            break
        response = str(request).upper().encode()

        yield ('write', client_socket)
        client_socket.send(response)

    client_socket.close()


def event_loop():
    while any([tasks, to_read, to_write]):
        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            # fill tasks with GENERATORS. dicts are pairs {socket: generator}
            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        try:
            # get task from "queue" of tasks
            task = tasks.pop(0)

            # destruct, because generator yields tuple of ('operation', socket)
            operation, sock = next(task)

            if operation == 'read':
                to_read[sock] = task
            elif operation == 'write':
                to_write[sock] = task

        except StopIteration:
            print('Done')


if __name__ == '__main__':
    tasks.append(server())
    event_loop()
