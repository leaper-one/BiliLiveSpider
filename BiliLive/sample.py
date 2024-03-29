import queue

import blivedm

# giftQueue = queue.Queue()
# 直播间ID的取值看直播间URL
TEST_ROOM_IDS = [
    7777,
]
# giftRecived = Queue()

# class consumer(Thread):
#     def __init__(self, queue):
#         Thread.__init__(self)
#         self.queue = queue
#
#         def run(self):
#             while True:
#                 gift = self.queue.get()
#                 print(gift)
#                 self.queue.take_done()

async def main(room, queue):
    await run_single_client(room, queue)


async def run_single_client(room, queue):
    """
    演示监听一个直播间
    """
    room_id = room
    # 如果SSL验证失败就把ssl设为False，B站真的有过忘续证书的情况
    client = blivedm.BLiveClient(room_id, ssl=True)
    handler = MyHandler(queue)
    client.add_handler(handler)

    client.start()
    try:
        await client.join()
    finally:
        await client.stop_and_close()

class MyHandler(blivedm.BaseHandler):

    def __init__(self, queue: queue.Queue):
        self.queue = queue
    # # 演示如何添加自定义回调
    # _CMD_CALLBACK_DICT = blivedm.BaseHandler._CMD_CALLBACK_DICT.copy()
    #
    # # 入场消息回调
    # async def __interact_word_callback(self, client: blivedm.BLiveClient, command: dict):
    #     print(f"[{client.room_id}] INTERACT_WORD: self_type={type(self).__name__}, room_id={client.room_id},"
    #           f" uname={command['data']['uname']}")
    # _CMD_CALLBACK_DICT['INTERACT_WORD'] = __interact_word_callback  # noqa
    #
    # async def _on_heartbeat(self, client: blivedm.BLiveClient, message: blivedm.HeartbeatMessage):
    #     print(f'[{client.room_id}] 当前人气值：{message.popularity}')
    #
    # async def _on_danmaku(self, client: blivedm.BLiveClient, message: blivedm.DanmakuMessage):
    #     print(f'[{client.room_id}] {message.uname}：{message.msg}')

    async def _on_gift(self, client: blivedm.BLiveClient, message: blivedm.GiftMessage):
        # print(f'[{client.room_id}] {message.uname} 赠送{message.gift_name}x{message.num}'
        #       f' （{message.coin_type}瓜子x{message.total_coin}）')
        # if message.coin_type != 'silver':
        self.queue.put([message.uid, message.price])
        print(self.queue.qsize())

    async def _on_buy_guard(self, client: blivedm.BLiveClient, message: blivedm.GuardBuyMessage):
        # print(f'[{client.room_id}] {message.username} 购买{message.gift_name}')
        self.queue.put([message.uid, message.price])
        print(self.queue.qsize())

    async def _on_super_chat(self, client: blivedm.BLiveClient, message: blivedm.SuperChatMessage):
        # print(f'[{client.room_id}] 醒目留言 ¥{message.price} {message.uname}：{message.message}')
        self.queue.put([message.uid, message.price])
        print(self.queue.qsize())
