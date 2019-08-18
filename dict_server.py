'''
服务端
多进程通信
'''
# 注册 R 登录 L 查单词 F 历史记录
import sys
import signal
from multiprocessing import Process
from socket import *
from database import *

# 防止僵尸进程产生
signal.signal(signal.SIGCHLD,signal.SIG_IGN)

HOST = '127.0.0.1'
PORT = 8000
ADDR = (HOST,PORT)

# 初始化套接字
sockfd = socket()
sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sockfd.bind(ADDR)
sockfd.listen(5)

# 创建数据库操作对象
db = Database()

# 注册
def do_register(c,name,passwd):
    if db.register(name,passwd):
        c.send(b'OK')
    else:
        c.send(b'NO')

# 登录
def do_login(c, name, passwd):
    if db.login(name,passwd):
        c.send(b'OK')
    else:
        c.send(b'NO')

# 查单词
def do_find(c, name, word):
    result = db.find_word(name,word)
    if result:
        c.send(result.encode())
    else:
        c.send(b'Fail')

# 查找历史记录
def do_history(c,name):
    msg = db.history(name)
    if msg:
        c.send(msg.encode())
    else:
        c.send(b'Not Found')

# 处理请求
def handle(c):
    while True:
        request = c.recv(1024).decode()
        if not request:
            c.close()
            sys.exit()
        # 注册
        if request[0] == 'R':
            tmp = request.split(' ')
            do_register(c,tmp[1],tmp[2])
        # 登录
        elif request[0] == 'L':
            tmp = request.split(' ')
            do_login(c,tmp[1],tmp[2])
        # 查单词
        elif request[0] == 'F':
            tmp = request.split(' ')
            do_find(c, tmp[1], tmp[2])
        # 查找历史记录
        elif request[0] == 'H':
            tmp = request.split(' ')
            do_history(c, tmp[1])

# 建立通信
def main():
    while True:
        # 循环接收来自客户端的请求
        c,addr = sockfd.accept()
        #采用多进程来处理具体请求
        p = Process(target=handle,args=(c,))
        p.daemon = True
        p.start()


if __name__ == '__main__':
    main()
    db.close()























