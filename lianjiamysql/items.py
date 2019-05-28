# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose

class FirstItemLoader(ItemLoader):
    #自定义itemloader，继承scrapy的ItemLoader类
    default_output_processor = TakeFirst()

def remove_m2(value):
    return value.replace('㎡', '').replace('暂无数据','0')

def remove_blank(value):
    return value.replace('\n', '').replace(' ', '').replace('暂无数据','NULL')

class LianjiamysqlItem(scrapy.Item):
    # define the fields for your item here like:
    zhandian = scrapy.Field()
    date = scrapy.Field()
    id = scrapy.Field()
    quyu = scrapy.Field()
    shangquan = scrapy.Field()
    xiaoqu = scrapy.Field()
    priceTotal = scrapy.Field()
    pricePerSqm = scrapy.Field()
    huxing = scrapy.Field()
    sqmTotal = scrapy.Field(input_processor=MapCompose(remove_m2))
    sqmInner = scrapy.Field(input_processor=MapCompose(remove_m2))
    chaoxiang = scrapy.Field()
    zhuangxiu = scrapy.Field()
    elevator = scrapy.Field(input_processor=MapCompose(remove_blank))
    floor = scrapy.Field()
    hxStructure = scrapy.Field(input_processor=MapCompose(remove_blank))
    leixing = scrapy.Field(input_processor=MapCompose(remove_blank))
    jzStructure = scrapy.Field()
    elevatorRatio = scrapy.Field(input_processor=MapCompose(remove_blank))
    nianxian = scrapy.Field()
    onlineDate = scrapy.Field()
    lastTradeDate = scrapy.Field()
    houseYear = scrapy.Field()
    diya = scrapy.Field(input_processor=MapCompose(remove_blank))
    quanshu = scrapy.Field()
    yongtu = scrapy.Field()
    chanquan = scrapy.Field(input_processor=MapCompose(remove_blank))
