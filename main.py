import threading
import queue
from giftAdder import Consumer
import spider
import time

# False 为运行， True 为停止
RoomIDStop = {
    "7777": False
}


# def consumer(queue: queue.Queue):
#     while True:
#         gift = giftRecived.get()
#         print(gift)
#         time.sleep(1)

if __name__ == '__main__':
    giftRecived = queue.Queue()

    t1 = threading.Thread(target=spider.KeepEyeOn, args=(
        7777, giftRecived, lambda: RoomIDStop["7777"],))
    t2 = threading.Thread(target=Consumer, args=(
        giftRecived, {}, lambda: RoomIDStop["7777"],))
    t1.start()
    t2.start()
    time.sleep(10) # 运行 10 秒
    # 结束线程
    RoomIDStop["7777"] = True
    t1.join()
    t2.join()
    print("main stop")
