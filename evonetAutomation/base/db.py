# -*- coding: utf-8 -*-

import pymysql
import cx_Oracle
from robot.api import logger
import random
import pymongo

from config.evopay.evopay_conf import EvopayConf


class Mysql_db():
    '''
    mysql数据库相关类
    '''
    # 游标#
    cur = ""
    # 数据库连接#
    conn = ""
    # 查询或者影响的行数#
    result_line = 0

    def __init__(self, host, user, passwd, db):
        # 初始化  主机IP，账号，密码，数据库的名字
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db

    def connentDB(self, db_type="mysql"):
        '''
                     预置条件：对象实例化
                     函数功能：连接数据库
                     参          数：无
                     返回值：无
        '''
        # 打开数据库连接
        if db_type == "mysql":
            self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db, port=3306,
                                        charset="utf8")
        elif db_type == "oracle":  # 看看能扩展为兼容宝行oracle ,现在不兼容
            self.conn = cx_Oracle.connect('swtonline', 'online', '192.168.1.234:1521/oradg', )
        # 使用cursor()方法获取操作游标；cursor() 方法创建一个游标对象 cursor
        self.cur = self.conn.cursor()
        logger.info("数据库连接成功")

    def executeSQL(self, sql, param=None):
        '''
                     预置条件：数据库连接成功
                     函数功能：执行增删改相关操作
                     参    数：param-参数，列表型；可以执行多条数据
                     返回值：无
        '''
        logger.info('即将执行的SQL操作语句：' + sql)
        if param is not None:
            count = 1
            param = tuple(param)
            for item in param:
                logger.info('参数' + str(count) + '：' + str(item))
                count += 1
        self.result_line = self.cur.execute(sql, param)
        logger.info("影响行数：" + str(self.result_line))

    def execute(self, sql):
        print(self.cur.execute(sql))

    def executeBatchSql(self, sql):
        '''
                     预置条件：数据库连接成功
                     函数功能：批量执行增删改相关操作
                     参          数：sql-sql语句，列表型，且为完整的sql
                     返回值：无
        '''
        logger.info('即将批量执行')
        for one in sql:
            self.executeSQL(one)
            self.commit()

    def getResultLine(self):
        '''
                     预置条件：执行完查询或者操作语句
                     函数功能：获取结果行数
                     参          数：无
                     返回值：查询结果行数
        '''
        return self.result_line

    def querySql(self, sql, param=None):
        '''
                     预置条件：数据库连接成功
                     函数功能：执行查询操作
                     参          数：param-参数，列表型
                     返回值：查询结果集，如果为空，返回None
        '''
        logger.info('即将执行的SQL查询语句：' + sql)
        if param is not None:
            count = 1
            param = tuple(param)
            for item in param:
                logger.info('查询参数' + str(count) + '：' + item)
                count += 1
        self.cur.execute(sql, param)
        result = self.cur.fetchall()
        if result == ():
            logger.info('未查询到相关结果')
            self.result_line = 0
            return None
        self.result_line = len(result)
        logger.info("查询到行数：" + str(len(result)))
        return result

    def commit(self):
        '''
                     预置条件：执行完数据库增删改操作
                     函数功能：提交
                     参          数：无
                     返回值：无
        '''
        logger.info('数据库提交')
        self.conn.commit()

    def curClose(self):
        '''
                     预置条件：数据库已经连接
                     函数功能：关闭游标
                     参          数：无
                     返回值：无
        '''
        logger.info('关闭游标')
        self.cur.close()
        self.cur = ""

    def connClose(self):
        '''
                     预置条件：数据库已经连接
                     函数功能：断开连接
                     参          数：无
                     返回值：无
        '''
        self.conn.close()
        logger.info('断开连接')

    def all_excetsql(self, sql, param=None):
        self.connentDB("mysql")  # 传默认参数
        self.executeSQL(sql, param)
        self.commit()
        self.curClose()
        self.connClose()


class oracle_db():
    '''
    oracle数据库相关类
    '''
    # 游标#
    cur = ""
    # 数据库连接#
    conn = ""
    # 查询或者影响的行数#
    result_line = 0

    def __init__(self, host, user, passwd, servce_name):
        # 初始化  主机IP，账号，密码，服务的名字
        self.host = host
        self.user = user
        self.passwd = passwd
        self.servce_name = servce_name

    def connentDB(self, db_type="mysql"):
        '''
                     预置条件：对象实例化 ;函数功能：连接数据库
                     参          数：mysql 代表连接mysql,oracle  代表连接oracle
        '''
        # 打开数据库连接
        if db_type == "mysql":
            self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db, port=3306,
                                        charset="utf8")
        elif db_type == "oracle":  # 看看能扩展为兼容宝行oracle ,现在不兼容
            self.conn = cx_Oracle.connect(self.user, self.passwd, self.host + ':1521/' + self.servce_name, )
        # 使用cursor()方法获取操作游标；cursor() 方法创建一个游标对象 cursor
        self.cur = self.conn.cursor()
        logger.info("数据库连接成功")

    def executeSQL(self, sql, param=None):
        '''
                     预置条件：数据库连接成功
                     函数功能：执行增删改相关操作;SQL statements should not contain a trailing semicolon (“;”) or forward slash (“/”). This will fail:
                     参    数：param-参数，列表型；可以执行多条数据
                     返回值：无
        '''
        logger.info('即将执行的SQL操作语句：' + sql)
        if param is not None:
            count = 1
            param = tuple(param)
            for item in param:
                logger.info('参数' + str(count) + '：' + str(item))
                count += 1
        self.result_line = self.cur.execute(sql, param)
        logger.info("影响行数：" + str(self.result_line))

    def execute(self, sql):
        # 执行sql的查询，insert,update,游标是操作sql,conn是连接并提交
        if sql.startswith("select"):
            # 执行sql ,一次查询，一次返回所有，
            self.cur.execute(
                sql)  # SQL statements should not contain a trailing semicolon (“;”) or forward slash (“/”). This will fail:
            rows = self.cur.fetchall()
            # for row in rows:
            #     print(row)
            return rows
        else:
            self.cur.execute(sql)

    def executeBatchSql(self, sql):
        '''
                     预置条件：数据库连接成功;函数功能：批量执行增删改相关操作
                     参          数：sql-sql语句，列表型，且为完整的sql
        '''
        logger.info('即将批量执行')
        for one in sql:
            if not one.startswith("select"):
                self.execute(one)
                self.commit()
            else:
                print("not select")

    def getResultLine(self):
        '''
                     预置条件：执行完查询或者操作语句
                     函数功能：获取结果行数
                     参          数：无
                     返回值：查询结果行数
        '''
        return self.result_line

    def commit(self):
        '''
                     预置条件：执行完数据库增删改操作
                     函数功能：提交
        '''
        logger.info('数据库提交')
        self.conn.commit()

    def curClose(self):
        '''
                     预置条件：数据库已经连接
                     函数功能：关闭游标
        '''
        logger.info('关闭游标')
        self.cur.close()
        self.cur = ""

    def connClose(self):
        '''
                     预置条件：数据库已经连接
                     函数功能：断开连接
        '''
        self.conn.close()
        logger.info('断开连接')


class MongoDB(object):
    '''
    操作mongoDB数据库
    '''

    def __init__(self, url, database):
        pymongo.write_concern.WriteConcern(w=3)
        # 连接数据库
        self.conn = pymongo.MongoClient(url)
        self.database = database

    def connect_url(self, url):
        # 连接数据库
        db = pymongo.MongoClient(url)
        return db

    # 查询语句
    def get_one(self, table, query_params):
        '''

    
        :param table: 数据表
        :param query_params: 查询语句
        :return:
        '''
        return self.conn[self.database][table].find_one(query_params)

        # 查询语句

    def get_many(self, table, query_params):
        '''


        :param table: 数据表
        :param query_params: 查询语句
        :return:
        '''
        return self.conn[self.database][table].find(query_params)

    # 更新语句
    def update_one(self, table, query_params, updata_params):
        '''

    
        :param table: 数据表
        :param query_params: 查询语句
        :param updata_params: 更新语句
        :return:
        '''
        return self.conn[self.database][table].update_one(query_params, {"$set": updata_params})

    def update_many(self, table, query_params, updata_params):
        '''


        :param table: 数据表
        :param query_params: 查询语句
        :param updata_params: 更新语句
        :return:
        '''
        return self.conn[self.database][table].update_many(query_params, {"$set": updata_params})

    def unset_many(self, table, query_params, unset_params):
        # unset_params  键值列表 如 ["key1","key2"]
        unset_dict = {}
        for i in unset_params:
            unset_dict[i] = ""
        return self.conn[self.database][table].update_many(query_params, {"$unset": unset_dict}, )

    # 删除语句
    def delete_one(self, table, query_params):
        '''

    
        :param table: 数据表
        :param query_params: 查询语句
        :return:
        '''
        return self.conn[self.database][table].delete_one(query_params)

    def delete_manys(self, table, query_params):
        '''
            删除多条数据
              :param table: 数据表
              :param query_params:
              :return:
              '''
        return self.conn[self.database][table].delete_many(query_params)

    # 插入语句
    def insert_one(self, table, insert_params):
        '''

    
        :param table: 数据表
        :param insert_params: 新增的语句
        :return:
        '''
        return self.conn[self.database][table].insert_one(insert_params)

    def insert_many(self, table, insert_params):
        '''


        :param table: 数据表
        :param insert_params: 新增的语句
        :return:
        '''
        return self.conn[self.database][table].insert_many(insert_params)

    # 计数
    def count(self, table, count_params):
        '''


        :param table: 数据表
        :param count_params: 新增的语句
        :return:
        '''
        return self.conn[self.database][table].count(count_params)

    def close_mongo(self):
        self.conn.close()

if __name__ == '__main__':
    evopay_conf = EvopayConf("test")
    # 初始化数据库
    db_tyo_evoconfig = MongoDB(evopay_conf.tyo_config_url, "evoconfig")
    db = db_tyo_evoconfig
    db.unset_many('customizeConfig', {"wopID":"WOP_Auto_JCoinPay_bilateral01"},["transCurrencies.0.mccr"])