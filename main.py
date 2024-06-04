from queue import Queue
from myasync import Consumer, Producer


def main():
    queue = Queue()

    producers = [Producer(queue=queue) for _ in range(3)]
    consumers = [Consumer(queue=queue) for _ in range(2)]

    for x in producers:
        x.start()
    for y in consumers:
        y.start()

if __name__ == "__main__":
    main()
