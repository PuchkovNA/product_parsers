# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import mongo_client

class ProductParsersPipeline:
    def __init__(self):
        CONNECTION_STRING = "mongodb://localhost:27018/local"
        mongo_cl=mongo_client.MongoClient(CONNECTION_STRING)
        self.mongo_db=mongo_cl.product_parser
    def process_item(self, item, spider):
        collection=self.mongo_db[spider.name]
        collection.insert_one(item)
        print('\n***************************\n%s\n%s\n***************************\n' % (
        item,spider))

        return item
