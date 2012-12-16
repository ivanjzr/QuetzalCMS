from quetzal import document as Doc
from quetzal.error import custom_errors as err
import web


#Authorization manager for this resource
from quetzal.authentication import operations as auth


#Schema instance
from api.admin_resources.modules import model
Module = model.Module


#Load Quetzal configuration
from quetzal import conf
quetzal_config = conf.QuetzalConfig.load()








######################## menus API ######################################
class ApiAdd(Doc.Json):

    def POST(self):
        #Authorization for this api is required
        try:
            curr_user = auth.auth_admin_res()
        except Exception as e:
            raise web.notfound()

        try:
            n_title = web.input(_method='post').title
            n_content = web.input(_method='post').content

            #Add new menu
            Module(
                title=n_title,
                contents=n_content
            ).save(force_insert=True)

            json_result = self.contents(dict(r='ok'))
            return json_result

        except Exception as e:
            return str(e)






class ApiEdit(Doc.Json):
    #path = '/edit/([a-zA-Z0-9_-]{3,50})'
    def POST(self):
        #Authorization for this api is required
        try:
            curr_user = auth.auth_admin_res()
        except Exception as e:
            raise web.notfound()

        try:
            oid = web.input(_method='post').oid
            n_title = web.input(_method='post').title
            n_content = web.input(_method='post').content

            #Update Query
            Module.objects(id=oid).update(
                set__title = n_title,
                set__contents = n_content
            )
            json_result = self.contents(dict(r='ok'))
            return json_result


        except Exception as e:
            raise StandardError(e)






class ApiDel(Doc.Json):
    def POST(self):
        #Authorization for this api is required
        try:
            curr_user = auth.auth_admin_res()
        except Exception as e:
            raise web.notfound()


        try:
            oid = web.input(_method='post').oid
            Module.objects(id=oid).delete()
            json_result = self.contents(dict(r="ok"))
            return json_result
        except Exception as e:
            raise web.notfound()