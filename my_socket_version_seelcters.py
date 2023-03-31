import socket
import selectors

selector = selectors.DefaultSelector()

def server():
    """
    Создание экземпляра серверного сокета.
    Установка опции SO_REUSEADDR для предотвращения ошибки "Address already in use".
    Привязка серверного сокета к заданному адресу и порту.
    Начало прослушивания входящих подключений.
    Регистрация серверного сокета в классе селекторов,
    ожидание события чтения (EVENT_READ) и вызов функции обратного вызова при возникновении этого события (accept_connectionn).
    Функция accept_connectionn должна быть определена отдельно и принимать один аргумент — объект сокета клиента.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('localhost', 8000)
    server_socket.bind(server_address)
    server_socket.listen()
    selector.register(
        fileobj=server_socket,
        events=selectors.EVENT_READ,
        data=accept_connectionn
        )


def accept_connectionn(server_socket):
    """
    Установка соединения с клиентом через метод accept() объекта server_socket.
    Вывод информации о подключившемся клиенте.
    Регистрация сокета клиента в классе селекторов для ожидания событий чтения (EVENT_READ)
    и вызовом функции обратного вызова (send_message) при возникновении события.
    Функция send_message должна быть определена отдельно и принимать один аргумент — объект сокета клиента.
    """
    client_socket, addr = server_socket.accept()
    print(f"Соединился с {addr}")
    selector.register(
        fileobj=client_socket,
        events=selectors.EVENT_READ,
        data=send_message
        )


def send_message(client_socket):
    """
    Получение запроса от клиента через метод recv() объекта client_socket.
    Если запрос получен, то:
    Открытие файла "response.txt" в режиме чтения.
    Чтение содержимого файла и отправка его клиенту через метод send()объекта client_socket.
    Вывод информации о том, что сервер ответил клиенту.
    Если запрос не получен, то:
    Снятие регистрации объекта client_socket из класса селекторов.
    Закрытие соединения с клиентом через метод close() объекта client_socket.
    Вывод информации о том, что сервер закрыт.
    Файл "response.txt" должен содержать ответ сервера в текстовом формате.
    """
    request = client_socket.recv(8096)
    if request:
        with open("response.txt", "r") as response_file:
            client_socket.send(response_file.read().encode())
            print(f"ответил серверу{client_socket}")
    else:
        selector.unregister(client_socket)
        client_socket.close(client_socket)
        print("сервер закрыт")


def event_loop():
    """
    Бесконечный цикл, который ожидает события в классе селекторов.
    Использование метода select() класса селекторов для получения списка пар "ключ-событие",
    которые имеют готовые данные для чтения или записи.
    Для каждого ключа в списке вызывается связанная с ним функция обратного вызова (callback),
    передавая ей соответствующий объект сокета в качестве аргумента.
    Вывод информации о вызываемой функции обратного вызова.
    """
    while True:
        events = selector.select()

        for key, _ in events:
            callback = key.data
            print(callback.__str__)
            callback(key.fileobj)


if __name__ == '__main__':
    server()
    event_loop()
