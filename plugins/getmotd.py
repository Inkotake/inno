from nonebot import on_command, CommandSession
import socket
import struct
import json
import time
class StatusPing:
    """ Get the ping status for the Minecraft server """

    def __init__(self, host='localhost', port=25565, timeout=5):
        """ Init the hostname and the port """
        self._host = host
        self._port = port
        self._timeout = timeout

    def _unpack_varint(self, sock):
        """ Unpack the varint """
        data = 0
        for i in range(5):
            ordinal = sock.recv(1)

            if len(ordinal) == 0:
                break

            byte = ord(ordinal)
            data |= (byte & 0x7F) << 7 * i

            if not byte & 0x80:
                break

        return data

    def _pack_varint(self, data):
        """ Pack the var int """
        ordinal = b''

        while True:
            byte = data & 0x7F
            data >>= 7
            ordinal += struct.pack('B', byte | (0x80 if data > 0 else 0))

            if data == 0:
                break

        return ordinal

    def _pack_data(self, data):
        """ Page the data """
        if type(data) is str:
            data = data.encode('utf8')
            return self._pack_varint(len(data)) + data
        elif type(data) is int:
            return struct.pack('H', data)
        elif type(data) is float:
            return struct.pack('Q', int(data))
        else:
            return data

    def _send_data(self, connection, *args):
        """ Send the data on the connection """
        data = b''

        for arg in args:
            data += self._pack_data(arg)

        connection.send(self._pack_varint(len(data)) + data)

    def _read_fully(self, connection, extra_varint=False):
        """ Read the connection and return the bytes """
        packet_length = self._unpack_varint(connection)
        packet_id = self._unpack_varint(connection)
        byte = b''

        if extra_varint:
            # Packet contained netty header offset for this
            if packet_id > packet_length:
                self._unpack_varint(connection)

            extra_length = self._unpack_varint(connection)

            while len(byte) < extra_length:
                byte += connection.recv(extra_length)

        else:
            byte = connection.recv(packet_length)

        return byte

    def get_status(self):
        """ Get the status response """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
            connection.settimeout(self._timeout)
            connection.connect((self._host, self._port))

            # Send handshake + status request
            self._send_data(connection, b'\x00\x00', self._host, self._port, b'\x01')
            self._send_data(connection, b'\x00')

            # Read response, offset for string length
            data = self._read_fully(connection, extra_varint=True)

            # Send and read unix time
            self._send_data(connection, b'\x01', time.time() * 1000)
            unix = self._read_fully(connection)

        # Load json and return
        response = json.loads(data.decode('utf8'))
        response['ping'] = int(time.time() * 1000) - struct.unpack('Q', unix)[0]

        return response


@on_command('motd', aliases=('动态贴图','motd') ,only_to_me=False)
async def lucky(session: CommandSession):
    litter = ':'
    yaoo = session.get('see', prompt='''=====by inkotake=====
请输入ip
例如: mc.hypixel.net
=====by inkotake=====''')

    result = litter in yaoo

    if result == True:
        ipport = yaoo.split(':')
        ip = "".join(ipport[0:1])
        port = "".join(ipport[1:])
        luck_back = await get_motd(ip,port)
        await session.send(luck_back)

    elif result == False:

        ip = yaoo

        luck_back = await get_motd(ip)
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


async def get_motd(ip,port):
    try:
        status_ping = StatusPing(host=ip, port=int(port))
        d = status_ping.get_status()


        a = '服务器ip：' + ip + '\n' + '最大人数：' + str(d['players']['max']) + '\n' + '在线人数：' + str(d['players']['online']) + '\n'+ '服务器版本：' + str(d['version']['name']) + '\n' + 'ping值:' + str(d['ping']) + '\n' + '服务器介绍:' +'\n'+ str(d['description']['text'] + '\n')

        return a
    except:
        try:
            status_ping = StatusPing(host=ip, port=int(port))

            d = status_ping.get_status()
            a = '服务器ip：' + ip + '\n' + '最大人数：' + str(d['players']['max']) + '\n' + '在线人数：' + str(
                d['players']['online']) + '\n' + '服务器版本：' + str(d['version']['name']) + '\n' + 'ping值:' + str(
                d['ping']) + '\n' + '服务器介绍:' + '\n' + str(d['description']['text'])
            print(d)
            return a
        except:

            try:
                status_ping = StatusPing(host=ip, port=int(port))

                d = status_ping.get_status()
                a = '服务器ip：' + ip + '\n' + '最大人数：' + str(d['players']['max']) + '\n' + '在线人数：' + str(d['players']['online']) + '\n'+ '服务器版本：' + str(d['version']['name']) + '\n' + 'ping值:' + str(d['ping']) + '\n' + '服务器介绍:' +'\n'+ str(d['description'])
                return a
            except:
                return '服务器无法访问或您的输入有误 有可能为mc服务器屏蔽本机ip'

async def get_motd2(ip):
    try:
        status_ping = StatusPing(ip)
        d = status_ping.get_status()
        a = '服务器ip：' + ip + '\n' + '最大人数：' + str(d['players']['max']) + '\n' + '在线人数：' + str(d['players']['online']) + '\n'+ '服务器版本：' + str(d['version']['name']) + '\n' + 'ping值:' + str(d['ping']) + '\n' + '服务器介绍:' +'\n'+ str(d['description']['text'])
        return a

    except:

        try:

            status_ping = StatusPing(ip)
            d = status_ping.get_status()
            print(d)
            a = '服务器ip：' + ip + '\n' + '最大人数：' + str(d['players']['max']) + '\n' + '在线人数：' + str(d['players']['online']) + '\n' + '服务器版本：' + str(d['version']['name']) + '\n' + 'ping值:' + str(d['ping']) + '\n' + '服务器介绍:' + '\n' + str(d['description'])

            return a

        except:
            return '此服务器无法访问 有可能为mc服务器屏蔽本机ip'