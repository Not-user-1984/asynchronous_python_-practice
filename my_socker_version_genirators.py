import socket
from select import select

tasks = []
to_read = {}
to_write = {}


def server():
    """
    Создание нового сокета server_socket.
    Установка опции SO_REUSEADDR для повторного использования адреса.
    Привязка сокета к адресу localhost:8000.
    Начало прослушивания входящих соединений.
    Бесконечный цикл, где используется ключевое слово yield 
    для генерации события 'read' и передачи server_socket как соответствующего сокета.
    Когда клиент пытается подключиться к серверу,
    операция accept() создает новый сокет client_socket,
    который принимает запрос от клиента.
    Добавление новой задачи client(client_socket) в стек задач tasks,
    которая будет выполнена асинхронно в дальнейшем.
    Функция client() будет обрабатывать запросы этого клиента.
    """

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('localhost', 8000)
    server_socket.bind(server_address)
    server_socket.listen()
    while True:
        print('ждем соединение..')
        yield('read', server_socket)
        client_socket, addr = server_socket.accept()
        print("соединение с ", addr)

        tasks.append(client(client_socket))


def client(client_socket):
    while True:
        yield('read', client_socket)
        request = client_socket.recv(8096)

        if not request:
            break
        else:
            with open("response.txt", "r") as response_file:
                yield('write', client_socket)
                client_socket.send(response_file.read().encode())
                print(f"ответил серверу{client_socket}")

    client_socket.close()
    print("сервер закрыт")


def event_loop():
    """
    Цикл начинается с проверки стеков задач tasks,
    to_read и to_write на наличие элементов.
    Если нет задач в стеках, он использует функцию select()
    для ожидания готовности к чтению или записи в один из сокетов в словарях to_read и to_write.
    Когда один из сокетов готов для чтения/записи
    он добавляет соответствующую задачу в стек tasks.
    Затем происходит извлечение первой задачи из стека tasks,
    и вызывается функция next() для генератора этой задачи.
    Она возвращает следующее событие (для чтения или записи) и соответствующий сокет.
    Затем сервер добавляет задачу обратно в соответствующий словарь (to_read или to_write)
    в зависимости от типа события.
    Если генератор заканчивает свою работу (генерирует StopIteration),
    это означает, что текущая задача выполнена, и сообщение "готово" выводится в консоль.
    Цикл продолжается до тех пор, пока в стеках tasks и to_read/to_write есть задачи на чтение или запись.
    """

    print("запуск...")
    while any([tasks, to_read, to_write]):
        print("задачи\n", tasks)
        print("на чтение\n", to_read)
        print("на запись\n", to_write)

        while not tasks:
            ready_to_read, ready_to_write, _ = select(
                to_read,
                to_write,
                []
                )
            for sock in ready_to_read:
                print('сокет на чтение\n',sock)
                tasks.append(to_read.pop(sock))

            for sock in ready_to_write:
                print('сокет на запись\n',sock)
                print(sock)
                tasks.append(to_write.pop(sock))

        try:
            task = tasks.pop(0)
            print(task)
            reason, sock = next(task)

            if reason == 'read':
                to_read[sock] = task

            if reason == 'write':
                to_write[sock] = task
        except StopIteration:
            print('готово')


if __name__ == '__main__':
    tasks.append(server())
    event_loop()