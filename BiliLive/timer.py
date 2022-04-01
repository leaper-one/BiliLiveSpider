from threading import Timer
import main
import rank
import requests
import asyncio

room = '4017751'
liveNum = 0

def live():
    r = requests.get(url="https://api.live.bilibili.com/room/v1/Room/room_init?id=" + room)
    liveStatus = r.json()['data']['live_status']
    if liveStatus == 0:
        Timer(15.0, live).start()
    elif liveStatus == 1 and liveNum == 0:
        lives = 1
        asyncio.get_event_loop().run_until_complete(main.main())
    elif liveStatus == 1 and liveNum == 1:
        rank()


def rank():
    pass