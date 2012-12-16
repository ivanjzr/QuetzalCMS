from quetzal import document as Doc
from quetzal.authentication import operations as auth_ops
import web

web.config.debug = False  #allow add mappings



#Login, logout & index mappings
urls = (
    #r'^/login/([a-zA-Z0-9_-]{3,8})/([a-zA-Z0-9_-]{3,8})$', "login",
    #r'/set_lang/([a-z_]{5})$', "switch_lang"
    "/login",    "login",
    "/index",    "index",
    "/logout",  "logout"
    )

#Api Application
app = web.application(urls, globals(), autoreload=None)




#------------------- mapped classes -----------------------------------

#from quetzal.url import page
#menus1 = page.loadJSONResults('http://idx-sb.com/api/2/menus/list')

class login(Doc.Json):
    def POST(self):
        try:
            web.header("Cache-Control", "no-cache, no-store, must-revalidate")
            #Use Post for Destructive actions such as Add/Edit and Delete
            #http://stackoverflow.com/a/46614/1747721

            #web.py: how to get POST parameter and GET parameter?
            #http://stackoverflow.com/a/10300958
            #http://webpy.org/cookbook/postbasic
            username = web.input(_method='post').username
            password = web.input(_method='post').password
            the_user = auth_ops.login(username, password)

            return self.contents(the_user)

        except Exception as e:
            return str(e)


#just call directly without Api Prefix
#i.e.: host/api/login
class logout(Doc.Json):
    def GET(self):
        try:
            logout_msg = auth_ops.logout()
            return self.contents(logout_msg)
        except Exception as e:
            return str(e)




class index(Doc.Json):
    def GET(self):
        try:
            the_user = auth_ops.auth_admin_res()
            return self.contents(the_user)
        except Exception as e:
            return str(e)