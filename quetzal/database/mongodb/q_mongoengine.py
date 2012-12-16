#Load Quetzal configuration
from quetzal import conf
quetzal_config = conf.QuetzalConfig.load()


#import mongoengine connection that will be used along the way
from mongoengine import connect

#--------------default values-------------
DEF_HOST    = "localhost"
DEF_DB      = "test"
DEF_PORT    = "27017"
DEF_USER    = ""
DEF_PWD     = ""

#-------------config values----------------
HOST    = quetzal_config['mongodb']['host']     if 'host' in quetzal_config['mongodb'] else DEF_HOST
DB      = quetzal_config['mongodb']['db']       if 'db' in quetzal_config['mongodb'] else DEF_DB
PORT    = quetzal_config['mongodb']['port']     if 'port' in quetzal_config['mongodb'] else DEF_PORT
USER    = quetzal_config['mongodb']['user']     if 'user' in quetzal_config['mongodb'] else DEF_USER
PWD     = quetzal_config['mongodb']['password'] if 'password' in quetzal_config['mongodb'] else DEF_PWD



#https://mongoengine-odm.readthedocs.org/en/latest/guide/connecting.html
def init():
    connect(DB, username=USER, password=PWD, host=HOST, port=PORT)