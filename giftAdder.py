import queue


def giftAdder(giftQueue: queue.Queue, re: dict) -> dict:
    if "amount" not in re:
        re = {"amount": 0}

    while re["amount"] < 10:
        try:
            gift = giftQueue.get(timeout=5)  # 阻塞 5 秒
            if gift[0] in re:
                re[gift[0]] += gift[1]
            else:
                re[gift[0]] = gift[1]

            re["amount"] += 1
        except queue.Empty:
            re.pop("amount")
            return re
        except Exception as e:
            return e

    re.pop("amount")
    return re


def Consumer(giftQueue: queue.Queue, re: dict, stopFlag: bool):
    print("Consumer start")
    while True:
        re = giftAdder(giftQueue, re)
        if re:
            print(re)
        if stopFlag():
            print("Consumer stop")
            break


if __name__ == '__main__':
    giftQueue = queue.Queue(0)
    for i in range(10):
        giftQueue.put({"uid": "001", "qn": 100})
    for i in range(10):
        giftQueue.put({"uid": "002", "qn": 150})

    re = Consumer(giftQueue, {}, False)
    print(re)
