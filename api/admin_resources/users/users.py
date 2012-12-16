from quetzal import document as Doc
from quetzal.authentication import operations as auth_ops
from api.admin_resources.users import model
import web




class ApiAdd(Doc.Json):
    def POST(self):
        #Authorization for this api is required
        try:
            curr_user = auth_ops.auth_admin_res()
        except Exception as e:
            raise web.notfound()
        try:
            #Get User data
            new_user = {
                "name": web.input(_method='post').name,
                "username":web.input(_method='post').username,
                "email":web.input(_method='post').email,
                "password":web.input(_method='post').password,
                "priv_lev":web.input(_method='post').priv_lev,
                "is_default":web.input(_method='post').deft
            }
            #get the results
            result, data = model.addUser(new_user)
            ret_obj = dict(r=result)
            ret_obj['data'] = data
            json_result = self.contents(ret_obj)
            return json_result

        except Exception as e:
            return str(e)


class ApiEdit(Doc.Json):
    def POST(self):
        #Authorization for this api is required
        try:
            curr_user = auth_ops.auth_admin_res()
        except Exception as e:
            raise web.notfound()

        try:
            #Get User data
            new_user = {
                "oid": web.input(_method='post').oid,
                "name": web.input(_method='post').name,
                "username":web.input(_method='post').username,
                "current_password":web.input(_method='post').current_password,
                "new_password":web.input(_method='post').new_password,
                "email":web.input(_method='post').email,
                "priv_lev":web.input(_method='post').priv_lev,
                "is_default":web.input(_method='post').deft
            }
            #get the results
            result, data = model.updateUser(new_user)

            ret_obj = dict(r=result)
            ret_obj['data'] = data
            json_result = self.contents(ret_obj)
            return json_result

        except Exception as e:
            return str(e)



#Enable add first admin It allows to add users without authentication
add_first_admin = False
class ApiAddAdmin(Doc.Json):
    def GET(self):
        try:
            if add_first_admin:
                #new user object from public data
                new_user = {
                    "name":"Ivan Juarez",
                    "username":"ivanjzr",
                    "email":"ivanjzr@gmail.com",#We need to email for recovery as well
                    "password":"abc123",
                    "priv_lev":2,
                    "is_default":'true'
                }
                added_user = model.addFirstUser(new_user)
                ret_obj = dict(r="ok")
                ret_obj['data'] = added_user
                json_result = self.contents(ret_obj)
                return added_user
            else:
                ret_obj = dict(r="disabled")
                json_result = self.contents(ret_obj)
                return json_result
        except Exception as e:
            raise web.notfound(e)



class ApiDel(Doc.Json):
    def POST(self):
        #Authorization for this api is required
        try:
            curr_user = auth_ops.auth_admin_res()
        except Exception as e:
            raise web.notfound()
        try:
            oid = web.input(_method='post').oid
            #get the results
            result, data = model.delUser(oid)

            ret_obj = dict(r=result)
            ret_obj['data'] = data
            json_result = self.contents(ret_obj)
            return json_result

        except Exception as e:
            raise web.notfound()