import datetime
import threading
import time
from queue import Queue


class UmlBlockQueueWorker(threading.Thread):
    def __init__(self, queue: Queue) -> None:
        super().__init__(daemon=True)
        self.queue = queue
        self.current = None


class Consumer(UmlBlockQueueWorker):
    def __init__(self, queue) -> None:
        super().__init__(queue)

    def run(self) -> None:
        while True:
            item = self.queue.get(block=False)
            self.current = item
            print(f"From consumer: {item}")
            time.sleep(5)


class Producer(UmlBlockQueueWorker):
    def __init__(self, queue) -> None:
        super().__init__(queue)

    def run(self):
        while True:
            self.queue.put(datetime.datetime.now())
            time.sleep(2)
