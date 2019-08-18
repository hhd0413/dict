'''
数据库操作
'''
import hashlib
import pymysql

# 加密专用盐
salt = b'.#06/'

class Database:
    def __init__(self):
        # 连接数据库
        self.db = pymysql.connect(host='localhost',
                             port = 3306,
                             user = 'root',
                             password = '123456',
                             database = 'dict',
                             charset = 'utf8')
        # 创建游标对象(操作数据库语句，获取查询结果)
        self.cur = self.db.cursor()

    def close(self):
        #  关闭游标和数据库
        self.cur.close()
        self.db.close()

    # 注册
    def register(self,name,passwd):
        # 密码加密
        passwd = self.encrypt(passwd)

        sql_1 = 'select * from user where name = "%s"'%name
        result = self.cur.execute(sql_1)
        # 已存在
        if result:
            return False
        sql_2 = 'insert into user (name,passwd) values(%s,%s)'
        self.cur.execute(sql_2,[name,passwd])
        self.db.commit()
        return True

    # 登录
    def login(self,name,passwd):
        passwd = self.encrypt(passwd)
        sql = 'select * from user where name = %s and passwd = %s'
        result = self.cur.execute(sql,[name,passwd])
        if result:
            return True
        return False

    # 查单词
    def find_word(self,name,word):
        sql = 'select mean from words where word = "%s"'%word
        self.cur.execute(sql)
        data = self.cur.fetchone()
        if not data:
            return
        self.add_hist(name,word)
        return data[0]

    # 密码加密
    def encrypt(self, passwd):
        hash = hashlib.md5(salt)
        hash.update(passwd.encode())
        passwd = hash.hexdigest()
        return passwd

    # 添加历史记录
    def add_hist(self,name,word):
        sql = 'insert into hist(name,word) values(%s,%s)'
        self.cur.execute(sql,[name,word])
        self.db.commit()

    # 查找历史记录
    def history(self,name):
        sql = 'select name,word,time from hist where name = "%s" order by time DESC limit 10'%name
        self.cur.execute(sql)
        data = self.cur.fetchall()
        msg = ''
        for name,word,time in data:
            msg += name+' '+word+' '+str(time)+'\n'
        return msg

if __name__ == '__main__':
    db = Database()
    print(db.history('zxc'))



















