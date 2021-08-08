import re
import json
import scrapy
from datetime import datetime

from ..items import ItemPerson
from helper.utils import clean_result, strip_tags
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode, urljoin


class GetPerson(scrapy.Spider):
    name = "GetPerson"
    start_urls = []
    curr_page = 0
    max_page = 2951

    custom_settings = {
        'LOG_LEVEL': 'ERROR',  # CRITICAL, ERROR, WARNING, INFO, DEBUG
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
        },
    }

    def parse(self, response):
        item = ItemPerson()
        
        item['id'] = self.curr_page
        item['scrap_date'] = datetime.today().strftime('%Y-%m-%d %H:%M')

        item['name'] = response.css('.entry-title::text').extract_first()
        item['description'] = response.css('.entry-content').extract()

        details_table = []
        for row in response.xpath('//*[@class="table"]//tr'):
            details_table.append({
                'i': row.xpath('td[1]//text()').extract_first(),
                'v': row.xpath('td[2]//text()').extract_first(),
            })

        item['details_table'] = details_table

        item['profile_pic'] = response.css(
            '#sidebar-left .wp-post-image::attr(src)').extract_first()
        
        images = response.css(
            '.thumbnails li a::attr(href)').extract()
        
        if images is None:
            item['images'] = "-"
        elif len(images) > 0:
            picked_images = []
            
            for i in images:
                if i.startswith('/person'):
                    continue
                else:
                    picked_images.append(i)
            item['images'] = json.dumps(picked_images)
        else:
            item['images'] = "-"
        
        print(item['id'],item['name'])
        yield item


        if self.curr_page < self.max_page:
            self.curr_page += 1 
            next_page_url = "https://www.bmdb.com.bd/person/" + str(self.curr_page) + "/"
            yield scrapy.Request(url=next_page_url, callback=self.parse)