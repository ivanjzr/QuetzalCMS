import web
from quetzal.database import dbs

#values for DBStore
db = dbs.DBS.dbStore('mysql')

class LoginSession:
    def __init__(self, user, login, priv_level):
        self.init_user = user
        self.ini_login = login
        self.ini_priv_lev = priv_level

    def DBStore(self,app):
        store = web.session.DBStore(db, 'sessions')
        session = web.session.Session(app, store,
            initializer={'user': self.init_user,'login':self.ini_login, 'priv_lev':self.ini_priv_lev}) #low level user (just login screen
        return session

    def DiskStore(self):
        pass
