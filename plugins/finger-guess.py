from nonebot import on_command, CommandSession
import sqlite3


@on_command('se', aliases=('sea') ,only_to_me=False)
async def lucky(session: CommandSession):
    yao = session.get('see', prompt='''请输入参数
━━━━━━━━━━━━━━
请输入要出的
剪刀，石头，布
例: /sea 石头
/sea list 查看排行榜
━━━━━━━━━━━━━━
inno v0.1 by inkotake''')
    #解析数据
    data = session.ctx
    qq = int(data['user_id'])
    at2 = "[CQ:at,qq={}]"
    at = at2.format(qq)
    name = str(data['sender']['nickname'])
    age = int(data['sender']['age'])
    #判断指令内容
    if yao == "list":
        luck_back = await getlist()
        await session.send(luck_back)
    else:
        luck_back = await get_yao(yao,name,qq,age)
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


#剪刀石头布主体
async def get_yao(yao,name,qq,age):
    import random, time

    punches = ['石头', '剪刀', '布']
    computer_choice = random.choice(punches)
    while yao not in punches:
        return '输入错误，请重新出拳：'
    if (computer_choice == '石头' and yao == '布') or (computer_choice == '布' and yao == '剪刀') or (computer_choice == '剪刀' and yao == '石头'):

        a = ('电脑出：' + str(computer_choice) + '  yeah，你赢了！')
        await setlist(qqnow=qq,name=name,age=age,win=1)
        return a

    elif computer_choice == yao:

        return '电脑出：' + str(computer_choice) + '  平局'

    else:

        return '电脑出：'+ str(computer_choice) +'  Oh,你输了'

#胜利添加到数据库
async def setlist(qqnow,name,age,win):

    conn = sqlite3.connect('plugins/data/database.db')
    cursor = conn.cursor()

    try:
        create_tb_cmd = '''
            CREATE TABLE IF NOT EXISTS USER
            (NAME TEXT,
            QQ INT,
            AGE INT,
            WIN INT);
            '''
        # 主要就是上面的语句
        cursor.execute(create_tb_cmd)

    except:
        print ("Create table failed")
        return False


    cursor.execute('SELECT qq FROM USER')
    qqlist = cursor.fetchall()
    qqlist2 = [line[0] for line in qqlist]
    a = qqnow in qqlist2

    if a == False:
        sql = 'insert into user (name,qq,age,win) values ("{}",{},{},{})'
        sql2 = sql.format(name,qqnow,age,win)

        cursor.execute(sql2)


    elif a == True:
        cursor.execute('select * from user')
        winlist = cursor.fetchall()

        winlist2 = {line2[1]: line2[2] for line2 in winlist}
        winmore = winlist2[qqnow] + win



        cursor.execute('update user set name = ? , win = ? , age = ? where qq = ?',(name,winmore,age,qqnow))


    conn.commit()
    cursor.close()
    conn.close()

#获取数据库胜局榜
async def getlist():

    conn = sqlite3.connect('plugins/data/database.db')
    cursor = conn.cursor()

    try:
        create_tb_cmd = '''
            CREATE TABLE IF NOT EXISTS USER
            (NAME TEXT,
            QQ INT,
            AGE INT,
            WIN INT);
            '''
        # 主要就是上面的语句
        cursor.execute(create_tb_cmd)

    except:
        print ("Create table failed")
        return False


    cursor.execute('SELECT * FROM USER ORDER BY WIN DESC LIMIT 10')
    qqlist = cursor.fetchall()
    person = {line[0] : str(line[2]) for line in qqlist}
    print(qqlist)




    none = True
    number = 0
    back = "胜局榜\n"

    for i in person:
        c = i.replace(" ", "")
        while none:
            number += 1
            break
        back += str(number) + "." + c + "：" + person[i] + "\n"
    return back