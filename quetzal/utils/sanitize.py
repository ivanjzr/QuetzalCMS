from quetzal.utils import serializers


def cursor_to_str(array_cursor):
    x = []
    for item in array_cursor:
        x.append(serializers.SerializeObjectToStr().encode(item))
    return x



def cursor_to_dict(array_cursor):
    x = []
    for item in array_cursor:
        x.append(serializers.SerializeObject(item))
    return x