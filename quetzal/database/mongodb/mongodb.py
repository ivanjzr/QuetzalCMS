#Load Quetzal configuration
from quetzal import conf
quetzal_config = conf.QuetzalConfig.load()




#import python-mongo driver
import pymongo

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

#https://github.com/mongolab/mongodb-driver-examples/blob/master/python/pymongo_simple_example.py
#http://api.mongodb.org/python/current/api/pymongo/connection.html
#https://groups.google.com/forum/?fromgroups=#!topic/mongodb-user/8cQoD67g1mg
def dbMongoDb():
    #Speciy host & port on connection
    connection = pymongo.Connection(HOST,PORT)
    #Select database ( it can also be specified in a third paramter following port right above)
    db = connection[DB]
    #We proceed to authentication
    db.authenticate(USER,PWD)
    return db