import re
import json
import scrapy
from datetime import datetime

from helper.utils import clean_result
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode, urljoin


class GetMovie(scrapy.Spider):
    name = "GetMovie"
    start_urls = []
    curr_page = 0
    max_page = 1902

    custom_settings = {
        'FEED_URI': 'db/movie.csv',
        'LOG_LEVEL': 'ERROR',  # CRITICAL, ERROR, WARNING, INFO, DEBUG
        'FEED_EXPORT_FIELDS': [
            'id',
            'name',
            'year',
            'release_date',
            'genere',
            'actors',
            'crew',
            'poster',
            'images',
            'details_table',
            
       
            'scrap_date',
        ],
    }

    def get_person_id(self, r, type=False):
        if not r:
            return "-"

        if type:
            return  r.split('/')[-3] + '/' + r.split('/')[-2]
        else:
            return  r.split('/')[-2]
       

    def parse(self, response):
        item = {}

        item['id'] = self.curr_page
        item['scrap_date'] = datetime.today().strftime('%Y-%m-%d %H:%M')

        item['name'] = clean_result(response.css(
            '.entry-title::text').extract_first())

        item['year'] = clean_result(response.css(
            '.entry-title a::text').extract_first())

        item['release_date'] = clean_result(response.css(
            'a~ .table td+ td').extract_first())

        item['genere'] = response.css('.alignleft li:nth-child(1) a::attr(href)').extract()

        for i, s in enumerate(item['genere']):
            item['genere'][i] = s.split("/")[-2]

        crew = []
        for row in response.xpath('//*[@class="table"]//tr'):
            value = self.get_person_id(row.xpath('td[2]/a/@href').extract_first())

            if value != "-":
                crew.append({
                    'i': row.xpath('td[1]//text()').extract_first(),
                    'p': value,
                })

        item['crew'] = crew

        actors = []
        for row in response.css('.main-actor-table tr'):
            value = self.get_person_id(row.xpath('td[2]/a/@href').extract_first())

            if value != "-":
                actors.append({
                    'p': self.get_person_id(row.xpath('td[2]/a/@href').extract_first()),
                    'c': row.xpath('td[3]//text()').extract_first(),
                })

        item['actors'] = actors

        
        details = []
        is_first = True
        for row in response.css('.alignleft li'):
            if is_first:
                is_first = False
                continue

            value = self.get_person_id(row.xpath('a/@href').extract_first(),True)

            if value != "-":
                details.append({
                    't': row.xpath('span/text()').extract_first(),
                    'v': value
                })

        item['details_table'] = details

        item['poster'] = response.css(
            '#sidebar-left .wp-post-image::attr(src)').extract_first()

        images = response.css(
            '.thumbnails li a::attr(href)').extract()

        if images is None:
            item['images'] = "-"
        elif len(images) > 0:
            picked_images = []

            for i in images:
                if i.startswith('/movie'):
                    continue
                else:
                    picked_images.append(i)
            item['images'] = json.dumps(picked_images)
        else:
            item['images'] = "-"


        print(item['id'],"/",self.max_page,' - ', item['name'])
        yield item

        if self.curr_page < self.max_page:
            self.curr_page += 1
            next_page_url = "https://www.bmdb.com.bd/movie/" + \
                str(self.curr_page) + "/"
            yield scrapy.Request(url=next_page_url, callback=self.parse)
