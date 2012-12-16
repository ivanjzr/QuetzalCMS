from quetzal.templating import templates
from quetzal.utils import serializers
from quetzal.error import custom_errors as err
import web

#Authorization manager for this resource
from quetzal.authentication import operations as auth


#Schema instance
from quetzal.schemas import users as users_schema
Users = users_schema.Users


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
            #
            users_list = []
            for user in Users.objects:
                user_obj = {}
                user_obj['id'] = serializers.SerializeObject(user.id)
                user_obj['name'] = serializers.SerializeObject(user.name)
                user_obj['username'] = serializers.SerializeObject(user.username)
                user_obj['email'] = serializers.SerializeObject(user.email)
                user_obj['priv_lev'] = serializers.SerializeObject(user.priv_lev)
                user_obj['is_default'] = serializers.SerializeObject(user.isdefault)
                users_list.append(user_obj)
            render = tmpl.render('users_index')
            return render.display(web.ctx.lang, users_list)
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
            render = tmpl.render('users_new')
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
            single_user = {}
            user = Users.objects.get(id=oid)
            single_user['id']           = serializers.SerializeObject(user.id)
            single_user['name']         = serializers.SerializeObject(user.name)
            single_user['username']     = serializers.SerializeObject(user.username)
            single_user['email']        = serializers.SerializeObject(user.email)
            single_user['priv_lev']     = serializers.SerializeObject(user.priv_lev)
            single_user['is_default']   = serializers.SerializeObject(user.isdefault)

            drop_box = [
                {
                    'key':2,'value':'Super Administrator'
                },
                {
                    'key':1,'value':'Administrator'
                },
                {
                    'key':0,'value':'User'
                }
            ]


            render = tmpl.render('users_edit')
            return render.display(web.ctx.lang, single_user, drop_box)

        except Exception as e:
            raise StandardError(e)

