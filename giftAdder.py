import queue

def GiftAdder(giftQueue:queue.Queue,re={}) -> dict:
    if "amount" not in re:
        re = {"amount": 0}

    while re["amount"]<20:
        try:
            gift = giftQueue.get(timeout=5) # 阻塞 5 秒
            if gift["uid"] in re:
                re[gift["uid"]] += gift["qn"]
            else:
                re[gift["uid"]] = gift["qn"]
                
            re["amount"]+=1
        except queue.Empty:
            re.pop("amount")
            return re
        except Exception as e:
            return e

    re.pop("amount")
    return re
    
if __name__ == '__main__':
    giftQueue = queue.Queue(0)
    for i in range(10):
        giftQueue.put({"uid":"001", "qn":100})
    for i in range(10):
        giftQueue.put({"uid":"002", "qn":150})

    re = GiftAdder(giftQueue)
    print(re)