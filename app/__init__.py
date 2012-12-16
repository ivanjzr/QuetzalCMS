import web
class index:
    def GET(self):
        raise web.seeother('/main/index')
