import scrapy

class ItemPerson(scrapy.Item):
    scrap_date = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    details_table = scrapy.Field()
    profile_pic = scrapy.Field()
    images = scrapy.Field()
   