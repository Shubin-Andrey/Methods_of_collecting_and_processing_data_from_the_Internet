from pymongo import MongoClient


class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacansy_280

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        print(item['salary'], 'pip')

        return item
