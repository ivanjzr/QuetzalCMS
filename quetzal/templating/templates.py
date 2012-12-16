from quetzal import conf
from quetzal import ctx
import web

quetzal_config = conf.QuetzalConfig.load()


#template_dir = quetzal_config['quetzal_dir'] + '\\server\\admin\\app\\templates'


class tmpl:
    def __init__(self, tmpl_location, base_dir=quetzal_config['quetzal_dir'], layout=None, globals=globals()):
        try:
            #Set directories
            self.base_dir = base_dir + '/server'
            self.template_location = tmpl_location
            self.layout = layout
            self.globals = globals

            #Set template context accordingly
            if ctx.caller() == "admin":
                self.template_context = '/admin/app'
            elif ctx.caller() == "app":
                self.template_context = '/app'

            #Set Final Path
            self.template_path = self.base_dir + self.template_context + self.template_location

        except Exception as e:
            raise EnvironmentError(e)




    def frender(self, tmpl_name):
        try:
            self.tmpl_display = web.template.frender(self.template_path + tmpl_name + '.html')
            return self
        except Exception as e:
            raise EnvironmentError(e)




    def render(self, tmpl_name):
        try:
            self.tmpl = web.template.render(self.template_path, base=self.layout, globals=self.globals)
            self.tmpl_display = getattr(self.tmpl, tmpl_name)
            return self

        except Exception as e:
            raise EnvironmentError(e)




    def display(self, *tmpl_content):
        try:
            return self.tmpl_display(*tmpl_content)
        except Exception as e:
            raise EnvironmentError(e)