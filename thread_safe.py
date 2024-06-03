"""FIFO queue."""

from queue import Queue
from random import choice, randint
import threading
import time

from absl import app, flags, logging

from common.emojis import PRODUCTS
from common.view import View

FLAGS = flags.FLAGS
flags.DEFINE_string("flag_name", "Default value", "Flag description.")

logging.set_verbosity(logging.DEBUG)
logging.get_absl_handler().setFormatter(None)


def main(_):
    buffer_queue = Queue()

    producer_speed = 3
    producer_count = 3

    consumer_speed = 3
    consumer_count = 2

    producers = [
        Producer(buffer_queue, producer_speed, PRODUCTS) for _ in range(producer_count)
    ]
    consumers = [Consumer(consumer_speed, buffer_queue) for _ in range(consumer_count)]

    for producer in producers:
        producer.start()

    for consumer in consumers:
        consumer.start()

    view = View(buffer_queue, producers, consumers)
    view.animate()


class Worker(threading.Thread):
    def __init__(self, buffer, speed) -> None:
        super().__init__(
            daemon=True
        )  # Doesn't block program from exiting when main is finished
        self.product = None
        self.speed = speed
        self.buffer = buffer
        self.working = False
        self.progress = 0

    @property
    def state(self):
        if self.working:
            return f"{self.product} {self.progress}%"
        return ":zzz: IDLE"

    def simulate_idle(self):
        self.product = None
        self.working = False
        self.progress = 0
        time.sleep(randint(1, 3))

    def simulate_work(self):
        self.working = True
        self.progress = 0
        delay = randint(1, 1 + 15 // self.speed)
        for _ in range(100):
            time.sleep(delay / 100)
            self.progress += 1


class Producer(Worker):

    def __init__(self, buffer, speed, products):
        super().__init__(buffer, speed)
        self.products = products

    def run(self):
        while True:
            self.product = choice(self.products)
            self.simulate_work()
            self.buffer.put(self.product)
            self.simulate_idle()


class Consumer(Worker):
    def __init__(self, speed, buffer):
        super().__init__(buffer, speed)

    def run(self):
        while True:
            self.product = self.buffer.get()
            self.simulate_work()
            self.buffer.task_done()
            self.simulate_idle()


if __name__ == "__main__":
    try:
        app.run(main)
    except KeyboardInterrupt as ki:
        print(f"INTERRUPT {ki}")
