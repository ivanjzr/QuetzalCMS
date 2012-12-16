from quetzal import document as Doc
from api.public_resources.ops import model
import web


class ApiContact(Doc.Json):
    def POST(self):
        try:
            fullname = web.input(_method='post').fullname
            email = web.input(_method='post').email
            msg = web.input(_method='post').msg
            data = model.sendmsg(fullname, email, msg)

            if not data == None:
                ret_obj = dict(r='ok')
                ret_obj['data'] = "MAIL_SENT"
                json_result = self.contents(ret_obj)
                return json_result

            ret_obj = dict(r='ok')
            json_result = self.contents(ret_obj)
            return json_result

        except Exception as e:
            raise web.notfound()