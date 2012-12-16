from quetzal.database.mongodb import mongodb as mongodb_db
from quetzal.database.mysql import mysql as mysql_db


class DBS:

    #Get Sql Database Driver: MySql, Oracle, Postgrees, SqlLite, and so on
    @staticmethod
    def getSqlDatabase(db_type):
        if db_type=='mysql':
            return mysql_db.dbMySql()

    #Get NoSql Database Driver: MongoDb, CouchDb, RavenDb and so on
    #List of recomended http://nosql-database.org/
    @staticmethod
    def getNoSqlDatabase(db_type):
        if db_type=='mongodb':
            return mongodb_db.dbMongoDb()


    #Return Database Store Type for sessions
    @staticmethod
    def dbStore(db_type):
        if db_type=='mysql':
            return mysql_db.dbStoreMySql








