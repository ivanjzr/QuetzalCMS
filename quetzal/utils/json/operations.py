from quetzal.utils import serializers as serializer
from quetzal.utils import simplejson


def unicode_to_json(unicode_dict):
    json_dict = simplejson.dumps(unicode_dict, cls=serializer.SerializeObjectToStr)
    return json_dict


def str_to_json(str):
    json_result = simplejson.dumps(mongo_dict)
    return json_result