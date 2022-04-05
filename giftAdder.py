
import queue
from func_timeout import func_timeout, FunctionTimedOut

re = {}

def giftAdder(giftQueue,re={}):
    if "amount" not in re:
        re = {"amount": 0}

    while giftQueue.empty() != True and re["amount"]<20:
        gift = giftQueue.get()
        if gift["uid"] in re:
            re[gift["uid"]] += gift["qn"]
        else:
            re[gift["uid"]] = gift["qn"]
            
        re["amount"]+=1

    re.pop("amount")
    return re
    
    
def GiftAdder(giftQueue,re={}): 
    try:
        re = func_timeout(10, giftAdder, args=(giftQueue,{}))
    except FunctionTimedOut:
        return re
        # for uid, qn in re.items():
            # pass # TODO:将 re 存入数据库
    except Exception as e:
        return e
    return re

if __name__ == '__main__':
    giftQueue = queue.Queue(0)
    for i in range(10):
        giftQueue.put({"uid":"001", "qn":100})
    for i in range(10):
        giftQueue.put({"uid":"002", "qn":150})

    re = GiftAdder(giftQueue)
    print(re)