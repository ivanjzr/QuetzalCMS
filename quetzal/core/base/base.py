from quetzal.core.base import mappings
from quetzal.database import dbs
from quetzal import conf
from quetzal.sessions import ses_config
import web

#Get Quetzal configuration
quetzal_config = conf.QuetzalConfig.load()


#Get config data
QUETZAL_DIR = quetzal_config['quetzal_dir']
#Get admin api url
ADMIN_API_URL = quetzal_config['admin_api_url']
#Get admin api url
API_CLASS_PREFIX = quetzal_config['api_class_prefix']
#Get api url
API_URL = quetzal_config['api_url']
#Set Debug errors True/False

web.config.debug = False  #turns off the reloader and allows add mappings

#Restart thread?, do not use in production
APACHE_RESTART = quetzal_config['apache_restart_thread']
if bool(APACHE_RESTART):
    from quetzal.core import reloader
    reloader.reload(QUETZAL_DIR)

#Initialize mongoengine connection instance
from quetzal.database.mongodb import q_mongoengine
q_mongoengine.init()


class BaseApplication(object):

    def __init__(self):

        #Initialize mappings manager and set main mappings
        self.mappings = mappings.Manager(self, API_URL, ADMIN_API_URL)
        #Initialize main web application here
        self.app = web.application(self.mappings.get_main_mappings(), fvars=globals())



        #All Mappings must be done before web application instance
        #Admin mappings
        self.mappings.add_map_resource('/server/admin/app', 'Admin', api_class_prefix=API_CLASS_PREFIX)
        #Api mappings
        self.mappings.add_map_resource('/server/api/admin_resources', 'ApiAdminResources', api_class_prefix=API_CLASS_PREFIX)
        self.mappings.add_map_resource('/server/api/private_resources', 'ApiPrivateResources', api_class_prefix=API_CLASS_PREFIX)
        self.mappings.add_map_resource('/server/api/public_resources', 'ApiPublicResources', api_class_prefix=API_CLASS_PREFIX)
        #Site mappings
        self.mappings.add_map_resource('/server/app', 'Site', api_class_prefix=API_CLASS_PREFIX)

        #Set new session with initializers
        db = dbs.DBS.dbStore('mysql')
        store = web.session.DBStore(db, 'sessions')
        #Start session
        self.session = web.session.Session(self.app, store,
            initializer={
                'userid': 'anonymous',
                'priv_lev':'',
                'authenticated':False,
                'language': quetzal_config['default_language']
            }
        )
        #Add login session & language hooks
        self.app.add_processor(web.loadhook(self.login_session_hook))
        self.app.add_processor(web.loadhook(self.language_session_hook))






    #Add authentication result to web ctx so we can use it in sub apps
    def login_session_hook(self):
        web.ctx.session = self.session






    def language_session_hook(self):
        selected_lang = web.ctx.session.language
        lang_path = 'i18n.' + selected_lang
        try:
            lang_module = __import__(lang_path, fromlist='*')
            #Assign language module to web ctx lang
            web.ctx.lang = lang_module.lang
            return
        except Exception as e:
            pass
        #default language: en-us
        from i18n import en_us as lang_module
        #Assign language module to web ctx lang
        web.ctx.lang = lang_module.lang
        return