import pymongo
import urllib.parse
from App.config import getConfiguration
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from plone.memoize import forever
config = getConfiguration()
configuration = config.product_config.get('mongodb', dict())
mongoserver = configuration.get('mongoserver')
mongoport = int(configuration.get('mongoport'))

@forever.memoize
def get_mongo_client():
    registry = getUtility(IRegistry)
    dbuser = registry['edi.course.browser.settings.IEdiCourseSettings.dbuser']
    dbpassword = registry['edi.course.browser.settings.IEdiCourseSettings.dbpassword']
    username = urllib.parse.quote_plus(dbuser)
    password = urllib.parse.quote_plus(dbpassword)
    mongoclient = pymongo.MongoClient('mongodb://%s:%s@%s:%s' % (username, password, mongoserver, mongoport))
    print(u'MongoClient instanziert')
    return mongoclient
