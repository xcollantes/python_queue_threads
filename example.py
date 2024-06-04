import asyncio
import datetime
from queue import Queue
from threading import Thread
import time


async def consumer(q: Queue):
    while True:
        if not q.empty():
            print(q.get())
        else:
            await asyncio.sleep(0)


def main():
    q: Queue = Queue()
    thread_stuff = Thread(target=consumer, args=(q,))
    thread_stuff.start()

    print("some other task")
    q.put(datetime.datetime.now())
    time.sleep(2)
    q.put(datetime.datetime.now())
    time.sleep(2)
    q.put(datetime.datetime.now())


if __name__ == "__main__":
    # asyncio.run(main())
    main()
