import pymongo
from zope.interface import Interface
from App.config import getConfiguration
from zope.component import getUtility
config = getConfiguration()
configuration = config.product_config.get('mongodb', dict())
mongoserver = configuration.get('mongoserver')
mongoport = int(configuration.get('mongoport'))

class IMongoConnection(Interface):
    """Mongo Connection"""


class MongoConnection(object):

    def __init__(self, host='localhost', port=27017):
        self.host = host
        self.port = port
        self.client = pymongo.MongoClient(self.host, self.port)


def setup_mongo():
    return MongoConnection(host=mongoserver, port=mongoport)


def get_mongo_client():
    return getUtility(IMongoConnection)
