from mongoengine import *

######################## System User Schemas ##########################
#Field Types
#https://mongoengine-odm.readthedocs.org/en/latest/apireference.html#mongoengine.UUIDField
class Users(Document):
    name        = StringField(min_length=1,max_length=128,required=True)
    email       = StringField(min_length=6,max_length=128,required=True)
    username    = StringField(min_length=6,max_length=64,required=True)
    salt        = StringField(required=True)
    hashed_pwd  = StringField(required=True)
    priv_lev    = IntField(max_value=2,required=True)
    userid      = StringField(required=True)
    tokens      = ListField()
    isdefault   = StringField(required=True)
    #Will use UUID Field and add in cryptography operations in next version
    #userid = UUIDField()