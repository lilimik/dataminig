import time
from pprint import pprint
from random import randint
from collections import deque
from threading import Thread


def stream():
    count = 0
    while not count == amount:
        count += 1
        value = randint(1, 1000)
        stream_deque.append(value)
        # time.sleep(0.2)


def main():
    count = 0
    summ = 0
    moment_0 = 0
    uniq = set()
    values = {}
    variables_range = amount // variables_count
    variables_range_list = list()
    [variables_range_list.append(randint(i * variables_range, (i + 1) * variables_range)) for i in
     range(variables_count)]
    while not count == amount:
        if stream_deque:
            mi = stream_deque.popleft()

            if mi not in uniq:  # 0 момент
                uniq.add(mi)
                moment_0 += 1

                # count - 1 момент

            if count in variables_range_list:  # 2 момент
                if mi not in values:
                    values[mi] = 1

            if mi in values:
                values[mi] += 1

            count += 1

    for value in values:
        summ += amount * (2 * values[value] - 1)

    moment_1 = amount
    moment_2 = summ//variables_count
    pprint(moment_0)
    pprint(moment_1)
    pprint(moment_2)


if __name__ == '__main__':
    amount = 1000000
    stream_deque = deque()
    variables_count = 100
    variables = list()
    stream_array = []

    th_stream = Thread(target=stream, args=())
    th_main = Thread(target=main, args=())
    th_stream.start()
    th_main.start()
    th_main.join()
