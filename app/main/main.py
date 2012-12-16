from app.main import model
from quetzal.templating import templates
from quetzal.authentication import operations
from quetzal.utils import serializers
from quetzal import conf
import web

#Load configuration
quetzal_config = conf.QuetzalConfig.load()


#Menus Schema Reference
Menus = model.Menus
Module = model.Module


def loadMenu():
    try:
        #
        menu_list = []
        for menu in Menus.objects:
            menu_obj = {}
            menu_obj['title'] = menu.title
            menu_obj['descr'] = menu.descr
            menu_obj['path'] = menu.path
            menu_list.append(menu_obj)
        return menu_list

    except Exception as e:
        #Just return an empty list
        return []
menus = loadMenu()



def loadModules():
    try:
        #
        mod_list = dict()
        for module in Module.objects:
            mod_obj = {}
            mod_obj['title'] = serializers.SerializeObject(module.title)
            mod_obj['contents'] = serializers.SerializeObject(module.contents)
            mod_list[serializers.SerializeObject(module.title)] = mod_obj
        return mod_list

    except Exception as e:
        #Just return an empty list
        return []
modules = loadModules()


def loadCopyrights():
    copyrights = " www.beonline.com.mx &copy; Todos los derechos reservados "
    return copyrights
copyrights = loadCopyrights()

admin_globals = {
    'date_str': web.datestr,
    'config': quetzal_config,
    'admin_api_url': quetzal_config['admin_api_url'],
    'menus': menus,
    'modules': modules,
    'copyrights': copyrights
}




#------------------- mapped classes -----------------------------------
tmpl = templates.tmpl('/templates', layout='layout', globals=admin_globals)





class ApiIndex:
    def GET(self):
        try:

            render = tmpl.render('index')
            return render.display(web.ctx.lang)
        except Exception as e:
            return str(e)

class ApiServicios:
    def GET(self):
        try:

            render = tmpl.render('servicios')
            return render.display(web.ctx.lang, modules)
        except Exception as e:
            return str(e)

class ApiContacto:
    def GET(self):
        try:

            render = tmpl.render('contacto')
            return render.display(web.ctx.lang, modules)
        except Exception as e:
            return str(e)

class ApiNosotros:
    def GET(self):
        try:

            render = tmpl.render('nosotros')
            return render.display(web.ctx.lang, modules)
        except Exception as e:
            return str(e)

class ApiPortafolio:
    def GET(self):
        try:

            render = tmpl.render('portafolio')
            return render.display(web.ctx.lang, modules)
        except Exception as e:
            return str(e)