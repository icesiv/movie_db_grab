import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from helper.get_proxy import refresh_proxy

class Scraper:
    def __init__(self):
        settings_file_path = 'data_grab.settings'
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.process = CrawlerProcess(get_project_settings())
   
    def run_spiders(self,spider, start_index , url):
        spider.start_urls = [(url + str(start_index) +'/') ]
        spider.curr_page = start_index
        
        self.spiders = spider
        self.process.crawl(self.spiders)
        self.process.start() 

