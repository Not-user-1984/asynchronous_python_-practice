from inspect import getgeneratorstate


def make_coroutine(func):
    """
    определяет декоратор coroutine,
    который преобразует обычную функцию в генератор-корутину.
    Корутина - это взаимодействующие процессы,
    которые могут приостанавливаться и возобновляться
    в определенных точках выполнения для обработки входных данных.
    Декоратор устанавливает начальное состояние генератора-корутины,
    отправляя ему значение None при помощи метода send().
    """
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g

    return inner


@make_coroutine
def average_coroutine():
    """
    Этот код определяет генератор-корутину average(),
    которая вычисляет среднее значение последовательности чисел.
    Генератор начинается с установки переменных count,summ и average в нуль или None. 
    Затем генератор ожидает получения нового значения через метод yield.
    После получения нового значения, генератор увеличивает значение count,
    добавляет значение к summ, пересчитывает среднее значение и сохраняет его в average.
    Генератор продолжает ждать следующего значения до тех пор, пока не будет прерван при помощи исключения StopIteration.
    Декоратор @coroutine из предыдущего кода превращает функцию average() в генератор-корутину и устанавливает начальное состояние генератора,
    отправляя ему значение None через метод send().
    Затем создается объект генератора x вызовом функции average().
    """
    count = 0
    summ = 0
    avarage = None

    while True:
        try:
            x = yield avarage
        except StopIteration:
            print('Done ')
        else:
            count += 1
            summ += x
            avarage = round(summ / count, 2)

x = average_coroutine()

print(getgeneratorstate(x))


@make_coroutine
def avarage_new():
    """
    Этот код очень похож на предыдущий, но есть одно отличие.
    В этом случае генератор-корутина average_new() включает инструкцию break,
    которая прерывает бесконечный цикл генератора при получении исключения StopIteration.
    Это позволяет закончить выполнение генератора,
    когда все значения были обработаны.
    Кроме того, генератор-корутина возвращает значение среднего после завершения работы,
    используя оператор return. Это означает,
    что после вызова исключения StopIteration, значение среднего будет возвращено,
    а не просто распечатано в консоль.
    """
    count = 0
    summ = 0
    avarage = None

    while True:
        try:
            x = yield avarage
        except StopIteration:
            print('Done ')
            break
        else:
            count += 1
            summ += x
            avarage = round(summ / count, 2)

    return avarage

y = avarage_new()
y.send(5)
y.send(7)

try:
    y.throw(StopIteration)
except StopIteration as e:
    print('Avarage', e.value)
