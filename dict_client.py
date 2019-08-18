'''
客户端
'''
# 注册 R 登录 L 查单词 F 历史记录

import getpass
import sys
from socket import *

ADDR = ('127.0.0.1',8000)

sockfd = socket()
sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sockfd.connect(ADDR)

# 注册
def register():
    while True:
        name = input('name:')
        passwd = getpass.getpass()
        passwd1 = getpass.getpass('again:')
        if ' ' in name or ' ' in passwd:
            print('姓名与密码不能带有空格')
            continue
        elif passwd != passwd1:
            print('两次输入密码不一致')
            continue
        elif passwd == '' or name == '':
            print('姓名或密码不能为空')
            continue
        break
    msg = 'R ' + name + ' ' + passwd
    sockfd.send(msg.encode())
    response = sockfd.recv(128).decode()
    if response == 'OK':
        return True
    else:
        return False

# 登录
def login(name):
    passwd = getpass.getpass()
    msg = 'L ' + name + ' ' + passwd
    sockfd.send(msg.encode())
    response = sockfd.recv(128).decode()
    if response == 'OK':
        return True
    else:
        return False

# 查单词
def find(name):
    while True:
        word = input('word(#退出):')
        if word == '#':
            break
        msg = 'F ' + name + ' ' + word
        sockfd.send(msg.encode())
        mean = sockfd.recv(1024).decode().strip()
        if mean == 'Fail':
            print('没有该单词')
        else:
            print('word:%s'%mean)

# 查找历史记录
def history(name):
    msg = 'H ' + name
    sockfd.send(msg.encode())
    response = sockfd.recv(1024).decode()
    if response == 'Not Found':
        print('没有历史记录')
    else:
        print(response)

# 二级界面
def sec_view(name):
    while True:
        print('''
            =======================
            1.查单词 2.历史记录 3.退出
            =======================
            ''')
        try:
            cmd = input('cmd:')
        except KeyboardInterrupt:
            sys.exit('谢谢使用')
        if cmd == '1':
            find(name)
        elif cmd == '2':
            history(name)
        elif cmd == '3':
            break
        else:
            print('请输入正确的命令')

# 主函数
def main():
    while True:
        print('''
            ==================
            1.注册 2.登录 3.退出
            ==================
            ''')
        try:
            cmd = input('cmd:')
        except KeyboardInterrupt:
            sys.exit('谢谢使用')
        if cmd == '1':
            if register():print('注册成功')
            else:print('注册失败')
        elif cmd == '2':
            name = input('name:')
            if login(name):
                # print('进入二级界面')
                print('登录成功')
                sec_view(name)  #进入二级界面
            else:
                print('登录失败')
                continue
        elif cmd == '3':
            sys.exit('谢谢使用')
        else:
            print('请输入正确命令')

if __name__ == '__main__':
    main()





















