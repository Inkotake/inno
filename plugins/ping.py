from nonebot import on_command, CommandSession
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

@on_command('ping', aliases=('ping',), only_to_me=False)
async def lucky(session: CommandSession):
    data = session.ctx
    qq = int(data['user_id'])
    at2 = "[CQ:at,qq={}]"
    at = at2.format(qq)
    ttxt = '''{} 请输入ping的域名
━━━━━━━━━━━━━━
example:
/ping baidu.com
━━━━━━━━━━━━━━
inno v0.1 by inkotake'''
    t = ttxt.format(at)
    yaoo = session.get('see', prompt=t)
    await session.send("正在执行中 请等待....")
    luck_back = await ping(yaoo,at)
    await session.send(luck_back)


@lucky.args_parser
async def _(session: CommandSession):
    strip = session.current_arg_text.strip()

    if session.is_first_run:
        if strip:
            session.state['see'] = strip
        return

    if not strip:
        session.pause('您干啥子')
    session.state[session.current_key] = strip

async def ping(host,at):
    #初始化浏览器
    options = Options()
    options.headless = True
    browser = webdriver.Chrome(chrome_options=options)
    try:
        api = "http://ping.chinaz.com/{}"
        truehost = api.format(host)
        browser.get(truehost)
        # Load page
        sleep(15)
        #解析页面
        html = browser.page_source
        li = BeautifulSoup(html,"lxml")
        #获取内容
        avg = li.find(class_='item', id='avg').text
        fast = li.find(class_='item', id='fast').text
        slow = li.find(class_='item', id='slow').text

        fast1 = fast[0:2]
        fast2 = fast[2:]
        slow1 = slow[0:2]
        slow2 = slow[2:]
        avg1 = avg[0:2]
        avg2 = avg[2:]
    #文本格式
        txt = '''{} ping测试完毕
━━━━━━━━━━━━━━
测试站点：{}
共计 122 个测试点
{}：{}
{}：{}
{}：{}
━━━━━━━━━━━━━━
inno v0.1 by inkotake'''
        re = txt.format(at, host, fast1, fast2, slow1, slow2, avg1, avg2)
        browser.close()
        return re


    except:

        browser.close()

    return "ping出现错误"