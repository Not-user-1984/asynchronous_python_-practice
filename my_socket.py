import socket
from select import select

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = ('localhost', 8000)
server_socket.bind(server_address)
server_socket.listen()

to_monitor = []

def accept_connectionn(server_soket):
        client_socket, addr = server_socket.accept()
        print(f"Соединился с {addr}")
        send_message(client_socket)
        to_monitor.append(client_socket)


def send_message(client_socket):
    request = client_socket.recv(8096)
    if request:
        with open("response.txt", "r") as response_file:
            client_socket.send(response_file.read().encode())
    else:
        print(f"Connection with {client_socket.laddr} closed.")
        client_socket.close()


def event_loop():
    while True:
        ready_to_read, _, _ = select(to_monitor, [],[])
        for sock in ready_to_read:
            if sock is server_socket:
                accept_connectionn(sock)
            else:
                send_message(sock)


if __name__ == '__main__':
    to_monitor.append(server_socket)
    accept_connectionn(server_socket)
    event_loop()
