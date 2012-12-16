from quetzal import document as Doc
from quetzal.error import custom_errors as err
import web


#Authorization manager for this resource
from quetzal.authentication import operations as auth


#Schema instance
from api.admin_resources.menus import model
Menus = model.Menus


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
            n_descr = web.input(_method='post').descr
            n_path = web.input(_method='post').path
            #Add new menu
            Menus(
                title=n_title,
                descr=n_descr,
                path=n_path
            ).save(force_insert=True)
            json_result = self.contents(dict(r='ok'))
            return json_result
        except Exception as e:
            raise web.notfound()


class ApiEdit(Doc.Json):
    #path = '/edit/([a-zA-Z0-9_-]{3,50})/([a-zA-Z0-9_-]{3,50})/([a-zA-Z0-9_-]{3,50})/([a-zA-Z0-9_-]{3,50})'
    def POST(self):
        #Authorization for this api is required
        try:
            curr_user = auth.auth_admin_res()
        except Exception as e:
            raise web.notfound()

        try:
            oid = web.input(_method='post').oid
            n_title = web.input(_method='post').title
            n_descr = web.input(_method='post').descr
            n_path = web.input(_method='post').path

            #Update Query
            Menus.objects(id=oid).update(
                set__title = n_title,
                set__descr = n_descr,
                set__path = n_path
            )
            json_result = self.contents(dict(r='ok'))
            return json_result
        except Exception as e:
            raise web.notfound()




class ApiDel(Doc.Json):
    def POST(self):
        #Authorization for this api is required
        try:
            curr_user = auth.auth_admin_res()
        except Exception as e:
            raise web.notfound()


        try:
            oid = web.input(_method='post').oid
            Menus.objects(id=oid).delete()
            json_result = self.contents(dict(r="ok"))
            return json_result
        except Exception as e:
            raise web.notfound()