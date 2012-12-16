import web
from quetzal.utils import simplejson
#https://hacks.mozilla.org/2011/03/the-shortest-image-uploader-ever/
#http://www.artima.com/weblogs/viewpost.jsp?thread=335549
#https://groups.google.com/forum/?fromgroups=#!topic/webpy/u60TWQxoEiI
#https://groups.google.com/forum/?fromgroups=#!topic/webpy/8msfBte41lA
#https://groups.google.com/forum/?fromgroups=#!topic/webpy/GFS7RjOwYVY
#web.header("Cache-Control", "no-cache, no-store, must-revalidate")

#----------------- main request for content type --------------
class Request:
    # base request class, set content_type in sub-class
    def __init__(self):
        web.header('Content-Type', self.content_type)
        web.header('Access-Control-Allow-Origin', '*')

#----------------- Default content types --------------
#Html, Text, Json, will encode/decode proper content type
class Html(Request):
    content_type = 'text/html'
    def contents(self,contents):
        return contents

class Text(Request):
    content_type = 'text/plain'
    def contents(self,contents):
        return contents

class Json(Request):
    content_type = 'application/json'
    def contents(self,contents):
        return simplejson.dumps(contents)


