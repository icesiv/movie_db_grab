import re

class DataGrabPipeline(object):
   
    def process_item(self, item, spider):
        # print(">>", item.get('title'))

        return item
