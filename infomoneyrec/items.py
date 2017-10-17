# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InfomoneyrecItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    title = scrapy.Field()
    subtitle = scrapy.Field()
    assunto = scrapy.Field()
    data = scrapy.Field()
    conteudo = scrapy.Field()
    url = scrapy.Field()
    main_url = scrapy.Field()
    other_url = scrapy.Field()
