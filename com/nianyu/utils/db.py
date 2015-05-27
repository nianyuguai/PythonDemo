# coding=utf-8
__author__ = 'lixiaojian'

import MySQLdb

class DB:

    error_code = ''  #MySQL错误号码
    _instance = None  #本类的实例
    _conn = None  #数据库conn
    _cur = None  #游标
    _TIMEOUT = 30  #默认超时30秒
    _timecount = 0

    def __init__(self, db_conf):
        """
        初始化连接，获取连接对象
        """
        try:
            self._conn = MySQLdb.connect(
                         host=db_conf['host'],
                         port=db_conf['port'],
                         user=db_conf['user'],
                         passwd=db_conf['passwd'],
                         db=db_conf['db'],
                         charset=db_conf['charset'])
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            error_msg = 'MySQL error : ', e.args[0], e.args[1]
            print error_msg

            # 如果没有超过预设超时时间，则再次尝试连接，
            if self._timecount < self._TIMEOUT:
                interval = 5
                self._timecount += interval
                time.sleep(interval)
                return self.__init__(db_conf)
            else:
                raise Exception(error_msg)
        self._cur = self._conn.cursor()
        self._instance = MySQLdb

    def query(self,sql):
        """
        select sql
        """
        try:
            self._cur.execute("SET NAMES utf8")
            result = self._cur.execute(sql)
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            print "MySQL error : ", e.args[0], e.args[1]
            result = False
        return result

    def update(self,sql):
        """
        update sql
        """
        try:
            self._cur.execute("SET NAMES utf8")
            result = self._cur.execute(sql)
            self._conn.commit()
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            print "数据库错误代码:",e.args[0],e.args[1]
            result = False
        return result

    def insert(self,sql):
        """
        :return:执行 INSERT 语句。如主键为自增长int，则返回新生成的ID
        """
        try:
            self._cur.execute("SET NAMES utf8")
            self._cur.execute(sql)
            self._conn.commit()
            return self._conn.insert_id()
        except MySQLdb.Error, e:
            self.error_code = e.args[0]
            return False

    def fetchAllRows(self):
        """
        :return:返回结果列表
        """
        return self._cur.fetchall()

    def fetchOneRow(self):
        """
        :return:返回一行结果，然后游标指向下一行。到达最后一行以后，返回None
        """
        return self._cur.fetchone()

    def getRowCount(self):
        """
        :return:获取结果行数
        """
        return self._cur.rowcount

    def commit(self):
        """
        数据库commit操作
        """
        self._conn.commit()

    def rollback(self):
        """
        数据库回滚操作
        """
        self._conn.rollback()

    def __del__(self):
        """
        释放资源（系统GC自动调用）
        """
        try:
            self._cur.close()
            self._conn.close()
        except:
            pass

    def  close(self):
        """
        关闭数据库连接
        """
        self.__del__()



if __name__ == '__main__':
    db_conf = {
        'host':'localhost',
        'port': 3306,
        'user':'root',
        'passwd':'',
        'db':'python',
        'charset':'utf8'
    }
    db = DB(db_conf)
    sql = "select * from test"
    db.query(sql)
    result = db.fetchAllRows()
    for r in result:
        print r

    db.close()