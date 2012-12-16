import random
from hashlib import sha1

import hashlib
import uuid
import base64, pickle



def get_base64_uuid4():
    result_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
    return result_uuid.replace('=', '')


def get_a_bunch_of_salt():
    return get_base64_uuid4()




def decode_base64(data):
    return base64.decodestring(data)





def transform_session_data(data):
    decoded_base64 = decode_base64(data)
    pickled_data = pickle.loads(decoded_base64)
    return pickled_data

