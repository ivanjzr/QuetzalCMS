from quetzal import document as Doc
import web


class ApiSwitchLanguage(Doc.Json):
    path = '/switch_language/([a-z_]{5})'
    def GET(self,selected_lang):
        try:
            web.ctx.session.language = selected_lang
            language = self.contents(dict(switched_to=selected_lang))
            return language
        except Exception as e:
            raise web.notfound()