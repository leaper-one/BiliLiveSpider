from tracemalloc import stop
import BiliLive.blivedm as blivedm
import queue
import asyncio

# taskType=[str,queue.Queue]

def KeepEyeOn(room_id:str, queue:queue.Queue, stopFlag:bool):
    loop = asyncio.new_event_loop()
    task = [run_single_client(room_id, queue, lambda: stopFlag())]
    try:
        loop.run_until_complete(asyncio.wait(task))
    finally:
        # print("loop close")
        loop.close()

async def run_single_client(room_id, queue, stopFlag:bool):
    """
    监听一个直播间
    """
    # 如果SSL验证失败就把ssl设为False，B站真的有过忘续证书的情况
    client = blivedm.BLiveClient(room_id, ssl=True)
    handler = MyHandler(queue)
    client.add_handler(handler)

    client.start()
    try:
        # await client.join()
        while True and client.is_running:
            if stopFlag():
                break
    finally:
        print("stop KeepEyeOn")
        await client.stop_and_close()


class MyHandler(blivedm.BaseHandler):

    def __init__(self, queue: queue.Queue):
        self.queue = queue

    async def _on_gift(self, client: blivedm.BLiveClient, message: blivedm.GiftMessage):
        # print(f'[{client.room_id}] {message.uname} 赠送{message.gift_name}x{message.num}'
        #       f' （{message.coin_type}瓜子x{message.total_coin}）')
        # if message.coin_type != 'silver':
        self.queue.put({'room_id':client.room_id, 'uid':message.uid, 'qn':message.price})
        # print(self.queue.qsize())

    async def _on_buy_guard(self, client: blivedm.BLiveClient, message: blivedm.GuardBuyMessage):
        # print(f'[{client.room_id}] {message.username} 购买{message.gift_name}')
        self.queue.put({'room_id':client.room_id, 'uid':message.uid, 'qn':message.price})
        # print(self.queue.qsize())

    async def _on_super_chat(self, client: blivedm.BLiveClient, message: blivedm.SuperChatMessage):
        # print(f'[{client.room_id}] 醒目留言 ¥{message.price} {message.uname}：{message.message}')
        self.queue.put({'room_id':client.room_id, 'uid':message.uid, 'qn':message.price})
        # print(self.queue.qsize())
