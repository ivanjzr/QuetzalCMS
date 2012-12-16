from mongoengine import *


######################## menus Schema ######################################


class Menus(Document):
    title = StringField(required=True)
    descr = StringField(max_length=150)
    path = StringField(max_length=50)