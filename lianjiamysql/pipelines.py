# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
import pymysql

class LianjiamysqlPipeline(object):
    def __init__(self):
        config = {
            'host': settings["MYSQL_HOST"],
            'port': settings["MYSQL_PORT"],
            'user': settings["MYSQL_USER"],
            'passwd': settings["MYSQL_PASSWD"],
            'db': settings["MYSQL_DBNAME"],
            'charset': 'utf8',
            'cursorclass': pymysql.cursors.DictCursor
        }

        self.conn = pymysql.connect(**config)
        self.conn.autocommit(1)

        #创建操作游标
        self.cursor = self.conn.cursor()

    def process_item(self,item,spider):
        if item.get('elevator'):
            pass
        else:
            item['elevator'] = 'NULL'
        if item.get('elevatorRatio'):
            pass
        else:
            item['elevatorRatio'] = 'NULL'
        if item.get('hxStructure'):
            pass
        else:
            item['hxStructure'] = 'NULL'
        if item.get('leixing'):
            pass
        else:
            item['leixing'] = 'NULL'
        if item.get('shangquan'):
            pass
        else:
            item['shangquan'] = 'NULL'

        sql = 'insert into lianjia_ershoufang values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %(item['zhandian'],item['date'],item['id'],item['quyu'],item['shangquan'],item['xiaoqu'],item['priceTotal'],item['pricePerSqm'],item['huxing'],float(item['sqmTotal']),float(item['sqmInner']),item['chaoxiang'],item['zhuangxiu'],item['elevator'],item['floor'],item['hxStructure'],item['leixing'],item['jzStructure'],item['elevatorRatio'],item['nianxian'],item['onlineDate'],item['lastTradeDate'],item['houseYear'],item['diya'],item['quanshu'],item['yongtu'],item['chanquan'])
        self.cursor.execute(sql)
        return item

    def close_spider(self,spider):
        # 关闭操作游标
        self.cursor.close()
        # 关闭数据库连接
        self.conn.close()