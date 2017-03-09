#------------------------------------------------------
# Name:        wpf
# Purpose:
# Author:      WJH
# Created:     2017-02-18 13:30
# Envi:        python3
#------------------------------------------------------

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from spider.items import WpfItem

import re

import logging


class ArcgisWpf(Spider):
    name = "arcgis_wpf"
    allowed_domains = ["developers.arcgis.com"]
    baseurl = "https://developers.arcgis.com/net/latest/wpf/api-reference//html/"
    start_urls = [baseurl + "R_Project_WinDesktop_LibRef.htm",]

    url_set = set([])

    download_item_type = ['class', 'enumeration', 'interface']


    def clear_str(self, str):
        rep_reg = re.sub(r'\r\n\s*', ' ', str)
        rep_reg = re.sub(r'\(\".*?\"\);', ' ', rep_reg)
        return rep_reg.strip()

    def get_wpf_item(self, title, title_type, selector):
        item = WpfItem()
        item['class_type'] = title_type.lower()
        item['class_name'] = title
        summary = selector.xpath('//div[@id = "TopicContent"]/div[@class = "summary"]')
        if len(summary) >0:
            item['class_desc'] = self.clear_str(summary.xpath("string(.)").extract()[0])
        item['namespace'] = selector.re(r'<strong>Namespace:</strong>.*?<a.*?>(.*?)</a>')[0]
        tr_infos = selector.xpath('//div[@class = "collapsibleSection"]/table[@class = "members"]//tr')
        tr_infos.extract()
        class_props = []

        for tr_info in tr_infos:
            class_prop = {}
            if title_type.lower() == 'enumeration' and len(tr_info.xpath("td").extract()) == 4:
                e_name = tr_info.xpath('td[2]')
                e_value = tr_info.xpath('td[3]')
                e_des = tr_info.xpath('td[4]')
                class_prop['name'] = self.clear_str(e_name.xpath("string(.)").extract()[0])
                class_prop['value'] = self.clear_str(e_value.xpath("string(.)").extract()[0])
                class_prop['desc'] = self.clear_str(e_des.xpath("string(.)").extract()[0])

            elif len(tr_info.xpath("td").extract()) == 3:
                c_type = tr_info.xpath('td[1]/img/@title').extract()[0]
                c_name = tr_info.xpath('td[2]')
                c_des = tr_info.xpath('td[3]/div[@class = "summary"]')

                class_prop['type'] = c_type
                class_prop['name'] = self.clear_str(c_name.xpath("string(.)").extract()[0])
                class_prop['desc'] = self.clear_str(c_des.xpath("string(.)").extract()[0])

            if len(class_prop) > 0:
                class_props.append(class_prop)

        item['class_props'] = class_props
        return item

    def parse(self, response):
        print(response.url)
        sel = Selector(response)
        titles_info = sel.xpath('//td[@class = "titleColumn"]/text()').extract()[0].split(' ')

        if len(titles_info) < 2:
            title_type = "class"
            self.log("class %s cant find type " % titles_info[0], logging.WARN)
        else:
            title_type = titles_info[1]
        title = titles_info[0]


        if title_type.lower() in self.download_item_type:
            yield self.get_wpf_item(title, title_type, sel)
        else:
            aurls = sel.xpath('//div[@class = "toclevel2"]/a/@href').extract()
            for next_url in aurls:
                if next_url == '#!' or next_url in self.url_set:
                    continue
                self.url_set.add(next_url)
                yield Request(self.baseurl + next_url, callback=self.parse)