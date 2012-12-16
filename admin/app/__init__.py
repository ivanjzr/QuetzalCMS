from quetzal.templating import templates
from quetzal.authentication import operations
from quetzal import conf
import web
web.config.debug = False  #allow add mappings


#Load configuration
quetzal_config = conf.QuetzalConfig.load()

admin_globals = {
    'admin_api_url': quetzal_config['admin_api_url']
}


urls = (
    "", "login_redirect",
    "/", "login_redirect",
    "/login", "login"

)

app = web.application(urls, globals())


#------------------- mapped classes -----------------------------------
tmpl = templates.tmpl('/templates', layout='layout', globals=admin_globals)


#Main Index already mapped
class login_redirect:
    def GET(self):
        web.seeother('/login')


#Main Index already mapped
class login:
    def GET(self):
        try:
            web.header("Cache-Control", "no-cache, no-store, must-revalidate")
            #If already logged successfully and user want to enter login again
            #just redirect to main index if is not authenticated just render login
            result = operations.authenticate()
            if result['r']=="ok":
                web.seeother('/main/index')
        except:pass
        try:
            render = tmpl.render("login")
            return render.display(web.ctx.lang)
        except Exception as e:
            return str(e)