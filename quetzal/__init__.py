#Initialize quetzal data and set restrictions to import only certain modules, in next version for efficient funcitonallity
#__all__("mod1","mod2","mod3")
from quetzal.core.base import base
import web


class QuetzalApplication(base.BaseApplication):
    def __init__(self):
        super(QuetzalApplication, self).__init__()
    def run(self):
        try:
            return self.app
        except Exception as e:
            return str(e)