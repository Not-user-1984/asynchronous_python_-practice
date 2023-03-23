import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = ('localhost', 8000)
server_socket.bind(server_address)
server_socket.listen()


while True:
    print('Жду клента...')
    client_socket, addr = server_socket.accept()
    print(f"Соединился с {addr}")

    while True:
        request = client_socket.recv(8096)

        if not request:
            break
        else:
            response = open("response.txt", "r")
            client_socket.send(response.read().encode())
    print(f"соединие c {addr} закрыл")