import datetime
import time
from queue import Queue


def main():
    q = Queue()
    do(q)
    consumer(q)


def do(q):
    message = datetime.datetime.now()
    print(f"FROM PRODUCER: {message}")
    q.put(message)
    time.sleep(2)


def consumer(q):
    print(f"FROM CONSUMER: {q.get()}")
    q.task_done()


if __name__ == "__main__":
    main()
