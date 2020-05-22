def gen1(n: int):
    for i in range(n):
        yield i


def gen2(s: str):
    for i in s:
        yield i


g1 = gen1(7)
g2 = gen2('m3xan1k')

tasks = [g1, g2]

while tasks:
    try:
        # take first task from "queue"
        task = tasks.pop(0)

        # execute task
        result = next(task)
        print(result)

        # move task to the end of queue
        tasks.append(task)
    except StopIteration:
        pass
