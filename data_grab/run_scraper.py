import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from helper.get_proxy import refresh_proxy

from data_grab.spiders.s_person import GetPerson

class Scraper:
    def __init__(self):
        settings_file_path = 'data_grab.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
   
    def run_spiders(self, start_index):
        spider = GetPerson
        self.process = CrawlerProcess(get_project_settings())
        # refresh_proxy()
        # spider.custom_settings['DOWNLOADER_MIDDLEWARES'].update({
        #     'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
        #     'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
        # })
        
        spider.start_urls = [('https://www.bmdb.com.bd/person/'+ str(start_index) +'/') ]
        spider.curr_page = start_index

        self.spiders = spider

        self.process.crawl(self.spiders)
        self.process.start() 