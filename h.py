import queue
import threading
import asyncio

def consume(myqueue):
    while True:
        try:
            item = myqueue.get(block=False)
        except queue.Empty:
            asyncio.sleep(0)
            continue
        yield item


q = queue.Queue()

def do(q):
    for item in consume(q):
        print(item)

thread = threading.Thread(target=do, args=(q,))

thread.start()

q.put("This")
q.put("is")
q.put("a test")
