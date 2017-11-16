from scrapy import Spider
from elasticsearch import Elasticsearch
from infomoneyrec.items import InfomoneyrecItem
from scrapy import Request
class InfomoneyRec(Spider):
    #define the name of the spider that will be runned 
    name = 'infomoneyrec'
    start_urls = ['http://www.infomoney.com.br/mercados/ultimas-noticias']
    allowed_domains = ['www.infomoney.com.br']   
    
    #define the method that your spider will scrapy the data from the urls declared on start_urls
    def parse(self, response):
        
        #count the id for the data scraped, that will be util on the elastic search
        id_elastic_index = 300  
        for quote in response.css('div.column'):
            item = InfomoneyrecItem()
            item['id_elastic_index'] = id_elastic_index
            item['main_url'] = response.url
            item['url'] = 'http://www.infomoney.com.br'+str(quote.css('div.section-box-secondary div.section-box-secondary-container-image a::attr(href)').extract_first())
            request = Request(str(item['url']),callback=self.parse_followpage)
            request.meta['item'] = item

            yield request
            
            id_elastic_index = id_elastic_index+1

    def parse_followpage(self, response): 
        es = Elasticsearch([{
            'host':'localhost',
            'port':9200,
        }])
        item = response.meta['item']
        item['title'] = response.css('h1.article__title::text').extract_first()
        item['subtitle'] = response.css('p.article__subtitle::text').extract_first()
        item['conteudo'] = response.css('div.article__content p::text').extract_first()
        item['other_url'] = response.url
        #es.index(index='testescrapy', doc_type='infomoney', id=)
        yield item
        es.index(index='testescrapy', doc_type='infomoney', id=int(item['id_elastic_index']), body={
            'Titulo':item['title'],
            'subtitle':item['subtitle'],
            'url':item['other_url'],
            'content':item['conteudo']
        })