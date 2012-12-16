#Load Quetzal configuration
from quetzal import conf
quetzal_config = conf.QuetzalConfig.load()
import web

#import mysql driver
import MySQLdb

#--------------default values-------------
DEF_HOST    = "localhost"
DEF_DB      = "test"
DEF_PORT    = "3306"
DEF_USER    = ""
DEF_PWD     = ""

#-------------config values----------------
HOST    = quetzal_config['mysql']['host'] if 'host' in quetzal_config['mysql'] else DEF_HOST
DB      = quetzal_config['mysql']['db'] if 'db' in quetzal_config['mysql'] else DEF_DB
PORT    = quetzal_config['mysql']['port'] if 'port' in quetzal_config['mysql'] else DEF_PORT
USER    = quetzal_config['mysql']['user'] if 'user' in quetzal_config['mysql'] else DEF_USER
PWD     = quetzal_config['mysql']['password'] if 'password' in quetzal_config['mysql'] else DEF_PWD


class dbMySql:
    def __init__(self):
        self.connection = MySQLdb.connect(host=HOST,user=USER,passwd=PWD,db=DB)

    #how to correctly do secured & scaped queries
    #http://stackoverflow.com/a/1307413
    def upsert(self,q,*params):
        try:
            cursor = self.connection.cursor()
            cursor.execute(q,*params)
            self.connection.commit()
        except Exception as e:
            return str(e)

    def fetch_all(self,q):
        try:
            cursor = self.connection.cursor()
            cursor.execute(q)
            return cursor.fetchall()
        except Exception as e:
            return str(e)

    def fetch_one(self,q,*params):
        try:
            cursor = self.connection.cursor()
            cursor.execute(q,*params)
            return cursor.fetchone()
        except Exception as e:
            return str(e)


dbStoreMySql = web.database(dbn='mysql', db=DB, user=USER, pw=PWD)