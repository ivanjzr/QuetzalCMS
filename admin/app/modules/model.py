from mongoengine import *


class Module(Document):
    title = StringField()
    contents = StringField()