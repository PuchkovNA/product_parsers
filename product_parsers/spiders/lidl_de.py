import scrapy
from scrapy.http import HtmlResponse

from product_parsers.items import ProductParsersItem


#from items import ProductParserItem


#from product_parser.items import ProductParserItem


class LidlDeSpider(scrapy.Spider):
    name = 'lidl_de'
    allowed_domains = ['lidl.de']
    start_urls = [
        'https://www.lidl.de/q/query/supersale?idsOnly=false&productsOnly=false&ratings=4+%26+mehr']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@class="s-load-more__button"]/@href').get()
        print(f'||||||||||||||||||||||||||||||||||||||||\n{next_page}\n||||||||||||||||||||||||||\n')
        if next_page:
            yield response.follow("https://www.lidl.de"+next_page, callback=self.parse)
            print(f'||||||||||||||||||||||||||||||||||||||||\n{next_page}\n||||||||||||||||||||||||||\n')
        product_links = response.xpath('//li[@class="s-grid__item"]//a/@href').getall()
        print(product_links)
        for link in product_links:
           # print(f'Yeeeee\n{link}')
            yield response.follow("https://www.lidl.de"+link, callback=self.parse_product)
        #print('\n==============================\n%s\n===============\n' % response.url)

    def parse_product(self, response: HtmlResponse):
        product_name = response.css('h1::text').get()
        print(f'Имя продукта ===============================================================\n{product_name}\n')
        product_url = response.xpath('//meta[@property="og:url"]/@content').get()
        product_price = response.css('div.m-price__price::text').get()
        print('\n***************************\n%s\n%s\n%s\n***************************\n' % (        product_name, product_url, product_price))
        #response.xpath('//span[@data-qa="vacancy-serp__vacancy-compensation"]/text()').getall()
        yield ProductParsersItem(product_name=product_name, product_url=product_url, product_price=product_price)
      #  print('\n***************************\n%s\n%s\n%s\n***************************\n' % (product_name, product_url,product_price))
