from scrapy import Spider
from elasticsearch import Elasticsearch
from infomoneyrec.items import InfomoneyrecItem
from scrapy import Request
class InfomoneyRec(Spider):
    name = 'infomoneyrec'
    start_urls = ['http://www.infomoney.com.br/mercados/ultimas-noticias']
    allowed_domains = ['www.infomoney.com.br']
    #def parse(self, response):
        #return Request("http://www.infomoney.com.br/mercados/politica/noticia/7023479/maia-diz-que-camara-vai-votar-nesta-terca-feira-urgencia",callback=self.parse_page2)
    #def parse_page2(self, response):
        #self.logger.info("visitado %s", response.url)
    
    def parse(self, response):
        es = Elasticsearch([{
            'host':'localhost',
            'port':9200,
        }])
        i = 1   
        for quote in response.css('div.column'):
            item = InfomoneyrecItem()
            item['main_url'] = response.url
            item['url'] = 'http://www.infomoney.com.br'+str(quote.css('div.section-box-secondary div.section-box-secondary-container-image a::attr(href)').extract_first())
            request = Request(str(item['url']),callback=self.parse_page2)
            request.meta['item'] = item
            yield request
            es.index(index='testescrapy', doc_type='infomoney', id = i, body={
                'title':item['title'],
                'subtitle':item['subtitle'],
                'url':item['other_url'],
            })
            i = i+1

    def parse_page2(self, response): 
        
        item = response.meta['item']
        item['title'] = response.css('h1.article__title::text').extract_first()
        item['subtitle'] = response.css('p.article__subtitle::text').extract_first()
        item['other_url'] = response.url
        yield item