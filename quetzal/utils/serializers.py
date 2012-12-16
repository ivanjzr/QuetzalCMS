from quetzal.utils.simplejson import JSONEncoder
from bson.objectid import ObjectId
import collections
import pymongo

#REFERENCES
#http://stackoverflow.com/a/11286887
#http://mumrah.net/24320734


#Serializer 1
def SerializeObject(data):
    if isinstance(data, unicode):
        return str(data)
    elif isinstance(data, ObjectId):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(SerializeObject, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(SerializeObject, data))
    else:
        return data


#Serializer 2
class SerializeObjectToStr(JSONEncoder):
    def default(self, obj, **kwargs):
        # convert object id to just id
        if isinstance(obj, ObjectId):
            return str(obj)
        # convert all iterables to lists
        elif hasattr(obj, '__iter__'):
            return list(obj)
        # convert cursors to lists
        elif isinstance(obj, pymongo.cursor.Cursor):
            return list(obj)
        # convert ObjectId to string
        elif isinstance(obj, pymongo.objectid.ObjectId):
            return unicode(obj)
        # dereference DBRef
        #elif isinstance(obj, pymongo.dbref.DBRef):
            #return db.dereference(obj)
        # convert dates to strings
        #elif isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date) or isinstance(obj, datetime.time):
            #return unicode(obj)
        return JSONEncoder.default(self, obj, **kwargs)