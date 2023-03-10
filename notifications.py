from data import data_to_notifications
from connect_psql import get_subscriptions
from bot import bot
import asyncio


async def notifications(delay):
    # while True:
    await asyncio.sleep(delay)
    data = data_to_notifications()
    if len(data) != 0:
        subscribers = get_subscriptions()
        for obj in subscribers:
            str_to_send = ''
            for tup in data:
                gx = tup[0]
                if type(tup[0]) == int:
                    gx = str(tup[0])
                if obj[2] == gx:
                    str_to_send += f'Ваш товар с треком {tup[1]} пришел!\n'
            if len(str_to_send) != 0:
                await bot.send_message(obj['user_id'], str_to_send)
asyncio.run(notifications(1))
