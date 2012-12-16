from quetzal.templating import templates
from quetzal.utils import serializers
from quetzal.error import custom_errors as err
import web

#Authorization manager for this resource
from quetzal.authentication import operations as auth


#Schema instance
from admin.app.modules import model
Module = model.Module



#Load Quetzal configuration
from quetzal import conf
quetzal_config = conf.QuetzalConfig.load()


t_globals = {
    'datestr': web.datestr,
    'admin_api_url': quetzal_config['admin_api_url']
}


tmpl = templates.tmpl('/main/templates', layout='layout', globals=t_globals)

#-------------------------- classes -------------------------------------





class ApiIndex:
    def GET(self):
        #Authorization for this resource is required
        try:
            curr_user = auth.auth_admin_res()
        except Exception as e:
            raise err.notfound()

        try:
            module_list = []
            for module in Module.objects:
                new_mod = {}
                new_mod['id'] = serializers.SerializeObject(module.id)
                new_mod['title'] = serializers.SerializeObject(module.title)
                new_mod['contents'] = serializers.SerializeObject(module.contents)
                module_list.append(new_mod)

            render = tmpl.render('modules_index')
            return render.display(web.ctx.lang, module_list)

        except Exception as e:
            raise StandardError(e)






class ApiNew:
    def GET(self):
        #Authorization for this resource is required
        try:
            curr_user = auth.auth_admin_res()
        except Exception as e:
            raise err.notfound()

        try:
            render = tmpl.render('modules_new')
            return render.display(web.ctx.lang)
        except Exception as e:
            raise StandardError(e)








class ApiEdit:
    path = '/edit/([a-zA-Z0-9_-]{3,50})'
    def GET(self, oid):
        #Authorization for this resource is required
        try:
            curr_user = auth.auth_admin_res()
        except Exception as e:
            raise err.notfound()

        try:
            #
            single_module = {}
            for module in Module.objects:
                if serializers.SerializeObject(module.id) == oid:
                    single_module['id'] = serializers.SerializeObject(module.id)
                    single_module['title'] = serializers.SerializeObject(module.title)
                    single_module['contents'] = serializers.SerializeObject(module.contents)

            render = tmpl.render('modules_edit')
            return render.display(web.ctx.lang, single_module)

        except Exception as e:
            raise StandardError(e)

