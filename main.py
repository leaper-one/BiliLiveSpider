import imp
import threading
import queue
import spider
import time



def consumer(queue: queue.Queue):
    while True:
        gift = giftRecived.get()
        print(gift)
        time.sleep(1)

if __name__ == '__main__':
    giftRecived = queue.Queue()

    t1 = threading.Thread(target=spider.KeepEyeOn, args=(7777, giftRecived, ))
    t2 = threading.Thread(target=consumer, args=(giftRecived, ))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    #TODO: 销毁线程