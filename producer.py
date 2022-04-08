import queue
import threading
from queue import Queue
import handler
import time

giftRecived = Queue()

def producer(room_id, queue: queue.Queue):
    handler.asyncMain(room_id, queue)

def consumer(queue: queue.Queue):
    while True:
        gift = giftRecived.get()
        print(gift)
        time.sleep(1)

if __name__ == '__main__':
    t1 = threading.Thread(target=producer, args=(7777, giftRecived, ))
    t2 = threading.Thread(target=consumer, args=(giftRecived, ))
    t1.start()
    t2.start()
    t1.join()
    t2.join()