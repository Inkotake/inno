from datetime import datetime

import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError
from time import sleep
sleep(10)


@nonebot.scheduler.scheduled_job('cron', hour='*')
async def _():
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    tt = r"[CQ:image,file=time\time ({}).jpg]"
    if int(now.hour) > 12:
        h = str(int(now.hour) - 12)
    else:
        h = now.hour
    time = tt.format(h)
    print(time)
    try:
        await bot.send_group_msg(group_id=1084282409,
                                 message=time)
        await bot.send_group_msg(group_id=872108566,
                                 message=time)
        await bot.send_group_msg(group_id=717701149,
                                 message=time)
    except CQHttpError:
        pass