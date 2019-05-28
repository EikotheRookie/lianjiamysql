# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from lianjiamysql.items import FirstItemLoader, LianjiamysqlItem
import re
from scrapy.conf import settings
import time

class LianjiaSpider(CrawlSpider):
    name = 'lianjiahouse'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://%s.lianjia.com/ershoufang//' %(settings['ZHANDIAN'])]

    rules = (
        Rule(LinkExtractor(allow=r'https://%s.lianjia.com/ershoufang/\d+.html' %(settings['ZHANDIAN'])),
             callback='parse_house', follow=True),
    )

    def parse_start_url(self, response):
        # 每个站的首页，爬取区域数
        url_navi_list = response.xpath(
            "/html/body/div[3]/div[@class='m-filter']/div[@class='position']/dl[2]/dd/div[1]/div[1]/a/@href").extract()
        for url_navi in url_navi_list:
            url_navi = 'https://%s.lianjia.com%s' % (settings['ZHANDIAN'], url_navi)
            yield scrapy.Request(url_navi, callback=self.parse_navi_url)

    def parse_navi_url(self, response):
        # 获取房源总页数
        body_data = response.body.decode('utf-8', 'ignore').replace(u'\xa9', u'').replace(u'\u2022', u'')
        rex = re.compile(r'\"page-data=\'\{\"totalPage\":(\d+),')
        totalpg = int(rex.findall(body_data)[0])
        for x in range(2, totalpg + 1):
            url_house = response.url + 'pg' + str(x) + '/'
            yield scrapy.Request(url_house)

    def parse_house(self, response):
        # 处理每一条房源信息，获取相应字段，保存到数据库
        item_loader = FirstItemLoader(item=LianjiamysqlItem(), response=response)
        item_loader.add_value('zhandian', settings['ZHANDIAN'])  #站点
        item_loader.add_value('date', time.strftime('%Y-%m-%d', time.localtime()))  #日期
        item_loader.add_xpath('id', '//*/div[@class="aroundInfo"]/div[@class="houseRecord"]/span[@class="info"]/text()')  #
        item_loader.add_xpath('quyu', '//*/div[@class="aroundInfo"]/div[@class="areaName"]/span[@class="info"]/a[1]/text()')  #
        item_loader.add_xpath('shangquan', '//*/div[@class="aroundInfo"]/div[@class="areaName"]/span[@class="info"]/a[2]/text()')  #
        item_loader.add_xpath('xiaoqu', '//*/div[@class="aroundInfo"]/div[@class="communityName"]/a[@class="info "]/text()')  #
        item_loader.add_xpath('priceTotal', '//span[@class="total"]/text()')  #
        item_loader.add_xpath('pricePerSqm', '//*/span[@class="unitPriceValue"]/text()')  #
        item_loader.add_xpath('huxing', '//*/div[@class="introContent"]/div[@class="base"]/div/ul/li/span[text()="房屋户型"]/../text()')  #
        item_loader.add_xpath('sqmTotal', '//*/div[@class="introContent"]/div[@class="base"]/div/ul/li/span[text()="建筑面积"]/../text()')  #
        item_loader.add_xpath('sqmInner', '//*/div[@class="introContent"]/div[@class="base"]/div/ul/li/span[text()="套内面积"]/../text()')  #
        item_loader.add_xpath('chaoxiang', '//*/div[@class="introContent"]/div[@class="base"]/div/ul/li/span[text()="房屋朝向"]/../text()')  #
        item_loader.add_xpath('zhuangxiu', '//*/div[@class="introContent"]/div[@class="base"]/div/ul/li/span[text()="装修情况"]/../text()')  #
        item_loader.add_xpath('elevator', '//*/div[@class="introContent"]/div[@class="base"]/div/ul/li/span[text()="配备电梯"]/../text()')  #
        item_loader.add_xpath('floor', '//*/div[@class="introContent"]/div[@class="base"]/div/ul/li/span[text()="所在楼层"]/../text()')  #
        item_loader.add_xpath('hxStructure', '//*/div[@class="introContent"]/div[@class="base"]/div/ul/li/span[text()="户型结构"]/../text()')  #
        item_loader.add_xpath('leixing', '//*/div[@class="introContent"]/div[@class="base"]/div/ul/li/span[text()="建筑类型"]/../text()')  #
        item_loader.add_xpath('jzStructure', '//*/div[@class="introContent"]/div[@class="base"]/div/ul/li/span[text()="建筑结构"]/../text()')  #
        item_loader.add_xpath('elevatorRatio', '//*/div[@class="introContent"]/div[@class="base"]/div/ul/li/span[text()="梯户比例"]/../text()')  #
        item_loader.add_xpath('nianxian', '//*/div[@class="introContent"]/div[@class="base"]/div/ul/li/span[text()="产权年限"]/../text()')  #
        item_loader.add_xpath('onlineDate', '//*/div[@class="introContent"]/div[@class="transaction"]/div/ul/li/span[text()="挂牌时间"]/../span[2]/text()')  #
        item_loader.add_xpath('lastTradeDate', '//*/div[@class="introContent"]/div[@class="transaction"]/div/ul/li/span[text()="上次交易"]/../span[2]/text()')  #
        item_loader.add_xpath('houseYear', '//*/div[@class="introContent"]/div[@class="transaction"]/div/ul/li/span[text()="房屋年限"]/../span[2]/text()')  #
        item_loader.add_xpath('diya', '//*/div[@class="introContent"]/div[@class="transaction"]/div/ul/li/span[text()="抵押信息"]/../span[2]/text()')  #
        item_loader.add_xpath('quanshu', '//*/div[@class="introContent"]/div[@class="transaction"]/div/ul/li/span[text()="交易权属"]/../span[2]/text()')  #
        item_loader.add_xpath('yongtu', '//*/div[@class="introContent"]/div[@class="transaction"]/div/ul/li/span[text()="房屋用途"]/../span[2]/text()')  #
        item_loader.add_xpath('chanquan', '//*/div[@class="introContent"]/div[@class="transaction"]/div/ul/li/span[text()="产权所属"]/../span[2]/text()')  #
        yield item_loader.load_item()
