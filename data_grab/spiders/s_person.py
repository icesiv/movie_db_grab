import re
import json
import scrapy
from datetime import datetime

from helper.utils import clean_result
# from urllib.parse import urlparse, parse_qs, urlunparse, urlencode, urljoin

class GetPerson(scrapy.Spider):
    name = "GetPerson"
    start_urls = []
    curr_page = 0
    max_page = 2951

    custom_settings = {
        'FEED_URI': 'db/person.csv',
        'LOG_LEVEL': 'ERROR',  # CRITICAL, ERROR, WARNING, INFO, DEBUG
        'FEED_EXPORT_FIELDS': [
            'id',
            'name',
            'profile_pic',
            'details_table',
            'description',
            'images',
            
            'acting',
            'direction',
            'writer',
            'art',
            'choreographer',
            'producer_person',
            'lyricist',
            'singer',
            
            'scrap_date',
        ],
    }
    
    def get_movie_info(self, r):
        if not r:
            return "-"

        movies = []
        links = r.css('li a::attr(href)').extract()

        for l in links:
            if l.find('/movie/') > 0:
                movies.append(l.split('/')[-2])
            
        return movies
        


    def parse(self, response):
        item = {}
        
        item['id'] = self.curr_page
        item['scrap_date'] = datetime.today().strftime('%Y-%m-%d %H:%M')

        item['name'] = clean_result(response.css('.entry-title::text').extract_first())
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
            
            
        item['acting'] = self.get_movie_info(response.css('#acting'))
        item['direction'] = self.get_movie_info(response.css('#direction'))
        item['writer'] = self.get_movie_info(response.css('#writer'))
        item['art'] = self.get_movie_info(response.css('#art'))
        item['choreographer'] = self.get_movie_info(response.css('#choreographer'))
        item['producer_person'] = self.get_movie_info(response.css('#producer_person'))
        item['lyricist'] = self.get_movie_info(response.css('#lyricist'))
        item['singer'] = self.get_movie_info(response.css('#singer'))
        
        print(item['id'],item['name'])
        yield item

        if self.curr_page < self.max_page:
            self.curr_page += 1 
            next_page_url = "https://www.bmdb.com.bd/person/" + str(self.curr_page) + "/"
            yield scrapy.Request(url=next_page_url, callback=self.parse)