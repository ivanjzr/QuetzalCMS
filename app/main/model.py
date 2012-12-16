from mongoengine import *



class Module(Document):
    title = StringField()
    contents = StringField()


class Menus(Document):
    title = StringField(required=True)
    descr = StringField(max_length=150)
    path = StringField(max_length=50)




