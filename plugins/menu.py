from nonebot import on_command, CommandSession
import os
import random


@on_command('menu', aliases=('菜单'),only_to_me=False)
async def lucky(session: CommandSession):
    yao = session.get('luckynumber', prompt='''下午好鸭~有什么可以帮您的吗
指令列表：
━━━━━━━━━━━━━━
/sea    人机猜拳
/motd   motd查询
/ping   ping检测
/vtb    vtb点歌
━━━━━━━━━━━━━━
inno v0.1 by inkotake''')

