from nonebot import on_command, CommandSession
import os
import random


@on_command('vtb', aliases=('vtb点歌'),only_to_me=False)
async def lucky(session: CommandSession):
    yao = session.get('luckynumber', prompt='''vtb点歌 by ink233
音乐资源来自于VTBMusic
指令列表(不需要/)：
━━━━━━━━━━━━━━
vtb点歌 歌曲名
vtbid点歌 歌曲ID
vtb歌手 歌手名
vtbhelp
━━━━━━━━━━━━━━
inno v0.1 by inkotake''')

