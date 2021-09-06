

# Data from departamentos en alquiler
# Scraping & Crawling en artículos

import os
from scrapy.item import Item, Field
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from fake_useragent import UserAgent
import random
import time
# pip install scrapy-rotating-proxies

from P1_Proxies import get_new_proxies

if os.path.exists('POS_PROXIES.txt'):
    pass
else:
    get_new_proxies()


class dataML(Item):

    ubicacion = Field()
    tipo = Field()
    moneda = Field()
    precio = Field()
    gmaps = Field()
    mcuad = Field()


class spiderML(CrawlSpider):

    name = 'alquileresML'

    rd_agent = UserAgent().random

    custom_settings = {
        'USER_AGENT': '{}'.format(rd_agent),
        # 'CLOSESPIDER_PAGECOUNT': 30, # for testing
        'FEED_EXPORT_ENCODING': 'iso-8859-1',
        'ROTATING_PROXY_LIST_PATH': r'POS_PROXIES.txt',
        'DOWNLOADER_MIDDLEWARES': {
            'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
            },
        'DUPEFILTER_DEBUG': True,
        'ROTATING_PROXY_CLOSE_SPIDER': False,
        'ROTATING_PROXY_PAGE_RETRY_TIMES': 20,
        'ROTATING_PROXY_LOGSTATS_INTERVAL': 10          
        }

    download_delay = random.uniform(2.0, 6.0)

    allowed_domains = [
        'listado.mercadolibre.com.pe', 
        'departamento.mercadolibre.com.pe',
        'terreno.mercadolibre.com.pe',
        'casa.mercadolibre.com.pe',
        'inmueble.mercadolibre.com.pe'
        ]

    start_urls = ['https://listado.mercadolibre.com.pe/inmuebles/alquiler/']
        

    rules = (
        Rule(LinkExtractor(allow=r'/_Desde_[0-9]*$'), follow=True),
        Rule(LinkExtractor(allow=r'/MPE-'), follow=True, callback='parse_items')
    )

    def limpiarTexto(self, texto):
        nuevoTexto = texto.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
        return nuevoTexto  

    def parse_items(self, response):
        item = ItemLoader(dataML(), response)

        time.sleep(random.uniform(2.0, 4.0))

        item.add_xpath('ubicacion', '//h3[@class="map-location"]/text()', MapCompose(self.limpiarTexto))
        item.add_xpath('tipo', '//article/dl/text()', MapCompose(self.limpiarTexto))
        item.add_xpath('moneda', '//span[@class="price-tag-symbol"]/text()')
        item.add_xpath('precio', '//span[@class="price-tag-symbol"]/@content')
        item.add_xpath('gmaps', '//div[@class="map-container map-container--dynamic"]/img[2]/@src')
        item.add_xpath('mcuad', '//dd[@class="align-surface"]/text()')

        yield item.load_item()
