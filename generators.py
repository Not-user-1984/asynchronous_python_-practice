def gen1(s):
    for i in s:
        yield i


def gen2(i):
    for i in range(i):
        yield i


g1 = gen1('Dima')

g2 = gen2(4)

tasks = [g1, g2]

while tasks:
    task = tasks.pop(0)

    try:
        i = next(task)
        print(i)
        tasks.append(task)
    except StopIteration:
        pass
