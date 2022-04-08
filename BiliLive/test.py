from threading import Thread, Event
import threading
from queue import Queue

class producer(Thread):
    def __init__(self, queue, giftRecived):
        Thread.__init__(self)
        self.queue = queue
        self.giftRecived = giftRecived

    def run(self):
        self.queue.put(self.giftRecived)
        print(self.giftRecived)

class consumer(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

        def run(self):
            while True:
                gift = self.queue.get()
                print(gift)
                self.queue.take_done()

if __name__ == '__main__':
    q = Queue()
    t1 = threading.Thread(target=producer, args=(q, ['1111', 90], ))
    t2 = threading.Thread(target=producer, args=(q, ['2222', 90], ))
    t3 = threading.Thread(target=producer, args=(q, ['3333', 90], ))
    t4 = threading.Thread(target=consumer, args=(q, ))

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()