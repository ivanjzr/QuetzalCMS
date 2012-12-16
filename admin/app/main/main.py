from quetzal.templating import templates
from quetzal.authentication import operations
from quetzal import conf
import web

#Load configuration
quetzal_config = conf.QuetzalConfig.load()



admin_globals = {
    'date_str': web.datestr,
    'config': quetzal_config,
    'admin_api_url': quetzal_config['admin_api_url']
}


#------------------- mapped classes -----------------------------------
tmpl = templates.tmpl('/main/templates', layout='layout', globals=admin_globals)


class ApiIndex:
    def GET(self):
        try:
            authorized_user = operations.authenticate()
            render = tmpl.render('main_index')
            return render.display(web.ctx.lang)
        except Exception as e:
            raise web.notfound()