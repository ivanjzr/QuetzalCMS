#http://webpy.org/cookbook/sessions_with_subapp
import web



class share_session:
    def __init__(self, app, session):
        self.session = session

    def session_hook(self):
        web.ctx.session = self.session

    def add_processor(self):
        app.add_processor(web.loadhook(self.session_hook))