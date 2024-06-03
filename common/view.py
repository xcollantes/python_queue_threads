# thread_safe_queues.py

from itertools import zip_longest
from queue import LifoQueue, PriorityQueue, Queue

from rich.align import Align
from rich.columns import Columns
from rich.console import Group
from rich.live import Live
from rich.panel import Panel

# ...


class View:
    def __init__(self, buffer, producers, consumers):
        self.buffer = buffer
        self.producers = producers
        self.consumers = consumers

    def animate(self):
        with Live(self.render(), screen=True, refresh_per_second=10) as live:
            while True:
                live.update(self.render())

    def render(self):

        match self.buffer:
            case PriorityQueue():
                title = "Priority Queue"
                products = map(str, reversed(list(self.buffer.queue)))
            case LifoQueue():
                title = "Stack"
                products = list(self.buffer.queue)
            case Queue():
                title = "Queue"
                products = reversed(list(self.buffer.queue))
            case _:
                title = products = ""

        rows = [Panel(f"[bold]{title}:[/] {', '.join(products)}", width=82)]
        pairs = zip_longest(self.producers, self.consumers)
        for i, (producer, consumer) in enumerate(pairs, 1):
            left_panel = self.panel(producer, f"Producer {i}")
            right_panel = self.panel(consumer, f"Consumer {i}")
            rows.append(Columns([left_panel, right_panel], width=40))
        return Group(*rows)

    def panel(self, worker, title):
        if worker is None:
            return ""
        padding = " " * int(29 / 100 * worker.progress)
        align = Align(padding + worker.state, align="left", vertical="middle")
        return Panel(align, height=5, title=title)


# ...
